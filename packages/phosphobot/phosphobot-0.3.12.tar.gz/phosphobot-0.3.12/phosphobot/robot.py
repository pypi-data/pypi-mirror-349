import ipaddress
import platform
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional, Set

import pybullet as p  # type: ignore
from fastapi import HTTPException
from loguru import logger
from scapy.all import ARP, Ether, srp  # type: ignore
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from phosphobot.configs import config
from phosphobot.hardware import (
    BaseRobot,
    KochHardware,
    PiperHardware,
    SO100Hardware,
    SO100LeaderHardware,
    UnitreeGo2,
    WX250SHardware,
)
from phosphobot.models import RobotConfigStatus
from phosphobot.utils import is_can_plugged

rcm = None


@dataclass
class NewAndOldPorts:
    new_ports: List[ListPortInfo]
    old_ports: List[ListPortInfo]
    new_can_ports: List[str]
    old_can_ports: List[str]


def fast_arp_scan(subnet="192.168.1.0/24", timeout=0.5):
    """
    Perform a fast ARP scan of the subnet to detect active hosts.
    """
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=subnet)
    packet = ether / arp

    answered, _ = srp(packet, timeout=timeout, verbose=False)
    devices = []

    for _, received in answered:
        devices.append({"ip": received.psrc, "mac": received.hwsrc.lower()})

    return devices


def slow_arp_scan(subnet="192.168.1.0/24", timeout=0.5, max_workers=64):
    """
    Parallelized ARP scan using ping and arp -a.
    Returns a list of {'ip': ..., 'mac': ...} entries.
    """
    ip_net = ipaddress.ip_network(subnet, strict=False)
    is_windows = platform.system().lower() == "windows"

    def ping_ip(ip_str):
        try:
            if is_windows:
                subprocess.run(
                    ["ping", "-n", "1", "-w", str(timeout), ip_str],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                subprocess.run(
                    ["ping", "-c", "1", "-W", str(int(timeout / 1000)), ip_str],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except Exception:
            pass  # Ignore ping errors

    logger.info(
        f"Pinging {ip_net.num_addresses} IPs in parallel (up to {max_workers} workers)..."
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(ping_ip, str(ip)) for ip in ip_net.hosts()]
        for _ in as_completed(futures):
            pass  # Wait for all pings to complete

    logger.info("Pings complete. Reading ARP table...")

    try:
        if is_windows:
            output = subprocess.check_output("arp -a", shell=True).decode()
            pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([\w-]+)\s+dynamic")
        else:
            output = subprocess.check_output(["arp", "-a"]).decode()
            pattern = re.compile(r"\(([\d.]+)\) at ([0-9a-f:]{17})", re.IGNORECASE)

        matches = pattern.findall(output)
        devices = [
            {"ip": ip, "mac": mac.lower().replace("-", ":")} for ip, mac in matches
        ]
        return devices

    except Exception as e:
        logger.error(f"Failed to read ARP cache: {e}")
        return []


class RobotConnectionManager:
    _all_robots: list[BaseRobot]
    _leader_robot: Optional[BaseRobot]

    robot_ports_without_power: Set[str]
    available_ports: List[ListPortInfo]
    available_can_ports: List[str]
    last_scan_time: float

    def __init__(self):
        self.available_ports = []
        self.available_can_ports = []
        self.robot_ports_without_power = set()
        self.last_scan_time = 0

        self._all_robots = []
        self._leader_robot = None

    def __del__(self):
        # Disconnect all robots
        for robot in self._all_robots:
            robot.disconnect()

    def _scan_ports(self) -> tuple[list, list]:
        """
        Scan USB and CAN ports.
        """
        # if os.name == "nt":  # Windows
        #     # List COM ports using pyserial
        #     ports = [port for port in list_ports.comports()]
        # else:  # Linux/macOS
        #     # List /dev/tty* ports for Unix-based systems
        #     # ports = [str(path) for path in Path("/dev").glob("tty*")]

        available_ports = list_ports.comports()

        # Look for CAN ports
        can_ports = []
        for i in range(2):  # Adjust based on maximum expected CAN interfaces
            can_name = f"can{i}"
            if is_can_plugged(can_name):
                can_ports.append(can_name)

        available_can_ports = can_ports
        self.last_scan_time = time.time()
        return available_ports, available_can_ports

    def difference_new_and_old_ports(
        self,
        new_ports: list[ListPortInfo],
        old_ports: list[ListPortInfo],
        new_can_ports: list[str],
        old_can_ports: list[str],
    ) -> NewAndOldPorts:
        """
        Make a difference between new and old ports.
        """
        # For ports, look at port.device for comparison
        new_ports_set = {port.device for port in new_ports}
        old_ports_set = {port.device for port in old_ports}

        # For CAN ports, look at the port name for comparison
        new_can_ports_set = set(new_can_ports)
        old_can_ports_set = set(old_can_ports)

        # Find the difference between the new and old ports
        new_ports_difference = new_ports_set.difference(old_ports_set)
        old_ports_difference = old_ports_set.difference(new_ports_set)

        # Find the difference between the new and old CAN ports
        new_can_ports_difference = new_can_ports_set.difference(old_can_ports_set)
        old_can_ports_difference = old_can_ports_set.difference(new_can_ports_set)

        return NewAndOldPorts(
            new_ports=[
                port for port in new_ports if port.device in new_ports_difference
            ],
            old_ports=[
                port for port in old_ports if port.device in old_ports_difference
            ],
            new_can_ports=list(new_can_ports_difference),
            old_can_ports=list(old_can_ports_difference),
        )

    def _find_robots(self) -> None:
        """
        Loop through all available ports and try to connect to a robot.

        Use self.scan_ports() before to update self.available_ports and self.available_can_ports
        """

        p.resetSimulation()
        self._all_robots = []

        # If we are only simulating, we can just use the SO100Hardware class
        if config.ONLY_SIMULATION:
            logger.debug("ONLY_SIMULATION is set to True. Using SO-100 in simulation.")
            self._all_robots = [SO100Hardware(only_simulation=True)]
            return

        # Keep track of connected devices by port name and serial to avoid duplicates
        connected_devices: Set[str] = set()
        connected_serials: Set[str] = set()

        # Try each serial port exactly once
        for port in self.available_ports:
            serial_num = getattr(port, "serial_number", None)
            # Skip if this port or its serial has already been connected
            if port.device in connected_devices or (
                serial_num and serial_num in connected_serials
            ):
                logger.debug(f"Skipping {port.device}: already connected (or alias).")
                continue

            for robot_class in [
                WX250SHardware,
                KochHardware,
                SO100Hardware,
                SO100LeaderHardware,
            ]:
                if not hasattr(robot_class, "name") or not hasattr(
                    robot_class, "from_port"
                ):
                    continue

                logger.debug(
                    f"Trying to connect to {robot_class.name} on {port.device}."
                )
                try:
                    robot = robot_class.from_port(
                        port,
                        robot_ports_without_power=self.robot_ports_without_power,
                    )
                except Exception as e:
                    logger.warning(
                        f"Error connecting to {robot_class.name} on {port.device}: {e}"
                    )
                    continue

                if robot is not None:
                    logger.success(f"Connected to {robot_class.name} on {port.device}.")
                    self._all_robots.append(robot)
                    # Mark both device and serial as connected
                    connected_devices.add(port.device)
                    if serial_num:
                        connected_serials.add(serial_num)
                    # Remove power-warning flag if present
                    self.robot_ports_without_power.discard(port.device)
                    break  # stop trying other classes on this port

        # Detect CAN-based Agilex Piper robots
        for can_name in self.available_can_ports:
            logger.info(f"Attempting to connect to Agilex Piper on {can_name}")
            robot = PiperHardware.from_can_port(can_name=can_name)
            if robot is not None:
                self._all_robots.append(robot)
                logger.success(f"Connected to Agilex Piper on {can_name}")

        # devices = None
        # try:
        #     devices = fast_arp_scan(subnet="192.168.1.0/24")
        # except PermissionError:
        #     logger.warning(
        #         "Can't run fast ARP scan. Please run as root or use sudo. Falling back to slow scan."
        #     )
        # except Exception as e:
        #     logger.error(f"ARP scan failed: {e}. Falling back to slow scan.")
        # if devices is None:
        #     devices = slow_arp_scan(subnet="192.168.1.0/24")

        # for device in devices:
        #     logger.debug(f"Found device: {device}")
        #     mac = device["mac"]
        #     ip = device["ip"]
        #     if any(
        #         mac.startswith(prefix) for prefix in UnitreeGo2.UNITREE_MAC_PREFIXES
        #     ):
        #         logger.success(f"Detected Unitree robot at {ip} with MAC {mac}")
        #         # You could initiate a connection attempt here if Unitree supports it (e.g., ping, TCP, or SSH)
        #         robot = UnitreeGo2.from_ip(ip=ip)
        #         if robot is not None:
        #             self._all_robots.append(robot)
        #         # Only 1 Go2 connection supported
        #         break

        if not self._all_robots:
            logger.info("No robot connected.")

    @property
    def robots(self) -> list[BaseRobot]:
        """
        Return all connected robots.
        """

        # In simulation, we call _find_robots() only once. It doesn't need to be updated.
        if config.ONLY_SIMULATION:
            if self._all_robots:
                return self._all_robots
            self._find_robots()
            return self._all_robots

        # If we are not in simulation, we check the ports
        if time.time() - self.last_scan_time > 1:
            logger.info("Scanning ports.")
            ports, can_ports = self._scan_ports()

            # If new ports are detected or old ports are deleted, we refresh the list of robots
            difference = self.difference_new_and_old_ports(
                ports, self.available_ports, can_ports, self.available_can_ports
            )
            if (
                difference.new_ports
                or difference.old_ports
                or difference.new_can_ports
                or difference.old_can_ports
                or self.robot_ports_without_power
            ):
                # First, disconnect all robots
                for robot in self._all_robots:
                    robot.disconnect()
                self.available_ports = ports
                self.available_can_ports = can_ports
                self._find_robots()

        # Return the stored list of robots
        return self._all_robots

    def get_robot(self, robot_id: int = 0) -> BaseRobot:
        """
        Return the currently connected robot.
        """
        robot = None

        if not isinstance(robot_id, int):
            raise ValueError("robot_id must be an integer.")

        if self._all_robots and len(self._all_robots) > robot_id:
            return self._all_robots[robot_id]

        robots = self.robots
        if robot_id >= len(robots):
            raise HTTPException(
                status_code=400,
                detail=f"Robot ID {robot_id} is out of range. Only {len(robots)} robots connected.",
            )

        robot = robots[robot_id] if robots else None
        if robot is None:
            raise HTTPException(
                status_code=400, detail=f"No robot with ID {robot_id} connected."
            )

        return robot

    def get_id_from_robot(self, robot: BaseRobot) -> int:
        """
        Return the ID of the robot.
        """

        return self._all_robots.index(robot)

    def status(self) -> list[RobotConfigStatus]:
        """
        Return the status of all robots. Used at server startup
        """
        robots_status = [robot.status() for robot in self.robots]
        # If a robot returned None, we disconnect it
        for status, robot in zip(robots_status, self.robots):
            if status is None:
                logger.warning(f"Robot {robot.name} is not connected. Disconnecting.")
                if hasattr(robot, "device_name") and robot.device_name is not None:
                    self.robot_ports_without_power.add(robot.device_name)

                robot.disconnect()
                self._all_robots.remove(robot)

        return [status for status in robots_status if status is not None]


@lru_cache()
def get_rcm() -> RobotConnectionManager:
    global rcm

    if rcm is None:
        rcm = RobotConnectionManager()

    return rcm
