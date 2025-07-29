import abc
import json
import random
import socket
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath
from threading import Thread
from typing import Callable, TypeAlias

from minitouchpy import utils

from . import const
from .logger import logger
from .utils import is_device_connected, is_port_using, str2byte

_read_callback_type: TypeAlias = Callable[[str], None]


def _check_install_mnt(
    deviceid: str,
    base_path: Path,
    mnthome="/data/local/tmp/minitouch",
    adb_executor=const.DEFAULT_ADB_EXECUTOR,
):
    """Check if minitouch is installed on the device and install it if missing.

    Args:
        deviceid (str): The unique identifier of the Android device.
        base_path (Path): Base directory containing compiled minitouch binaries. The structure should follow:
            base_path/{ABI}/minitouch or base_path/{ABI}/minitouch-nopie
            where {ABI} is the device's CPU architecture (e.g., armeabi-v7a, arm64-v8a).

    Raises:
        FileNotFoundError: If the minitouch binary cannot be found in the specified base_path/ABI directory.
    """
    file_list = subprocess.check_output(
        [
            adb_executor,
            "-s",
            deviceid,
            "shell",
            "ls",
            str(PurePosixPath(mnthome).parent),
        ]
    )
    if not PurePosixPath(mnthome).name in file_list.decode(const.DEFAULT_CHARSET):
        abi = subprocess.getoutput(
            "{} -s {} shell getprop ro.product.cpu.abi".format(adb_executor, deviceid)
        )
        logger.info("device {} is {}".format(deviceid, abi))

        mnt_path = base_path / abi / "minitouch"
        if not mnt_path.exists():
            raise FileNotFoundError("minitouch not found in {}".format(mnt_path))

        # push and grant
        subprocess.check_call([adb_executor, "-s", deviceid, "push", mnt_path, mnthome])
        subprocess.check_call(
            [adb_executor, "-s", deviceid, "shell", "chmod", "777", mnthome]
        )
        logger.debug("minitouch installed in {}".format(mnthome))
    else:
        logger.debug("minitouch already installed in {}".format(deviceid))


def _read_std(p: subprocess.Popen, callback: _read_callback_type):
    logger.debug("reading std thread started for process {}".format(p.pid))
    while p.poll() is None:
        line = p.stderr.readline()
        line = line.strip()
        if line:
            callback(line)


def _read_socket(sock: socket.socket, callback: _read_callback_type):
    logger.debug("reading socket thread started")
    buffer = ""
    while True:
        chunk = sock.recv(1).decode()
        if not chunk:
            break

        buffer += chunk
        if chunk == "\n":
            line = buffer.strip()
            buffer = ""
            callback(line)


class MNTServerCommunicateType(Enum):
    SOCKET = 0
    STDIO = 1


class MNTContextStatus(Enum):
    ESTABLISHED = "est"
    CLOSED = "cls"


class MNTEvent(Enum):
    PROTOCOL_VERSION = "v"
    DEVICE_INFO = "^"
    PID = "$"

    EVATIVE7_LOG = "jlog"
    EVATIVE7_CTX = "ctx"


@dataclass
class MNTEventData(abc.ABC):
    pass


@dataclass
class MNTProtocolVersionEventData(MNTEventData):
    version: int


@dataclass
class MNTDeviceInfoEventData(MNTEventData):
    max_contacts: int
    max_x: int
    max_y: int
    max_pressure: int


@dataclass
class MNTPIDEventData(MNTEventData):
    pid: int


@dataclass
class MNTEvATive7LogEventData(MNTEventData):
    start_time: float
    end_time: float
    cost: float
    cmd: str


@dataclass
class MNTEvATive7ContextEventData(MNTEventData):
    status: MNTContextStatus


class MNT(object):
    """Classes that manage minitouch services and are responsible for touch interactions with Android devices

    Args:
        device_id (str): Unique device identification
        type_ (str, optional): minitouch type, default "origin"
        communicate_type (MNTServerCommunicateType, optional): Communication method, SOCKET or STDIO, default SOCKET
        additional_param (list, optional): Additional parameter list, empty list by default. A list of parameters should be passed in, such as ["-v"]. Parameters managed internally by the class cannot be passed in, including "-n", "-i", "-f"
        callback (Callable[[MNTEvent, MNTEventData], None], optional): Event callback function, default None
    """

    _PORT_SET = const.PORT_SET
    _DEFAULT_HOST = const.DEFAULT_HOST

    def __init__(
        self,
        device_id,
        *args,
        type_="origin",
        communicate_type=MNTServerCommunicateType.SOCKET,
        additional_param=[],
        callback: Callable[[MNTEvent, MNTEventData], None] = None,
        mnt_asset_path: str = Path("."),
        adb_executor=const.DEFAULT_ADB_EXECUTOR,
        **kwargs,
    ):
        assert is_device_connected(device_id, adb_executor)

        self.device_id = device_id
        self.max_contacts = None
        self.max_x = None
        self.max_y = None
        self.max_pressure = None
        self.pid = None
        self._connected = False
        self.adb_executor = adb_executor

        self.type_ = type_
        self._additional_param = additional_param
        self._callback = callback
        self._communicate_type = communicate_type

        self.id_ = "minitouch_" + self.type_ + "_" + utils.generate_random_string(7)

        if self._communicate_type == MNTServerCommunicateType.STDIO:
            self._additional_param.append("-i")
        elif self._communicate_type == MNTServerCommunicateType.SOCKET:
            logger.info("searching a usable port ...")
            self.port = self._get_port()
            self.client = None
            logger.info("device {} bind to port {}".format(device_id, self.port))
            self._forward_port()

        self._additional_param += ["-n {}".format(self.id_)]
        self._additional_param = list(set(self._additional_param))
        self._mnt_home = "/data/local/tmp/{}".format("minitouch_" + self.type_)

        _check_install_mnt(
            device_id,
            mnt_asset_path,
            mnthome=self._mnt_home,
            adb_executor=self.adb_executor,
        )

        # keep minitouch alive
        self.mnt_process = None
        self._start_mnt()

        # make sure it's up
        time.sleep(1)
        assert (
            self.heartbeat()
        ), "minitouch did not work. see https://github.com/williamfzc/pyminitouch/issues/11"

        if self._communicate_type == MNTServerCommunicateType.SOCKET:
            self._connect()

    def stop(self):
        self.mnt_process and self.mnt_process.kill()
        if self._communicate_type == MNTServerCommunicateType.SOCKET:
            self._remove_forward_port()
        logger.info("stopped")

    def send(self, content):
        if self._communicate_type == MNTServerCommunicateType.STDIO:
            self.mnt_process.stdin.write(content)
        elif self._communicate_type == MNTServerCommunicateType.SOCKET:
            self.client.sendall(str2byte(content))

    @classmethod
    def _get_port(cls):
        """get a random port from port set"""
        new_port = random.choice(list(cls._PORT_SET))
        if is_port_using(new_port):
            return cls._get_port()
        return new_port

    def _connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self._DEFAULT_HOST, self.port))
        self.client = client

        logger.debug("connecting")

        Thread(target=_read_socket, args=(self.client, self._process_callback)).start()

    def _forward_port(self):
        """allow pc access minitouch with port"""
        command_list = [
            self.adb_executor,
            "-s",
            self.device_id,
            "forward",
            "tcp:{}".format(self.port),
            "localabstract:{}".format(self.id_),
        ]
        logger.debug("forward command: {}".format(" ".join(command_list)))
        output = subprocess.check_output(command_list, text=True)
        logger.debug("forward output: {}".format(output))

    def _remove_forward_port(self):
        """allow pc access minitouch with port"""
        command_list = [
            self.adb_executor,
            "-s",
            self.device_id,
            "forward",
            "--remove",
            "tcp:{}".format(self.port),
        ]
        logger.debug("remove forward command: {}".format(" ".join(command_list)))
        output = subprocess.check_output(command_list, text=True)
        logger.debug("remove forward output: {}".format(output))

    def _process_callback(self, line: str):
        try:
            logger.debug("recv event: {}".format(line))
            type_, data = line.strip().split(" ", 1)
            try:
                type_ = MNTEvent(type_)
            except ValueError:
                logger.debug("skip parsing event: {}: not found".format(line))
                return

            if type_ == MNTEvent.PROTOCOL_VERSION:
                data = MNTProtocolVersionEventData(int(data))
            elif type_ == MNTEvent.DEVICE_INFO:
                data = data.split(" ")
                data = MNTDeviceInfoEventData(*map(int, data))
            elif type_ == MNTEvent.PID:
                data = MNTPIDEventData(int(data))
            elif type_ == MNTEvent.EVATIVE7_LOG:
                data = json.loads(data)
                data = MNTEvATive7LogEventData(
                    start_time=data["st"],
                    end_time=data["et"],
                    cost=data["c"],
                    cmd=data["cmd"],
                )
            elif type_ == MNTEvent.EVATIVE7_CTX:
                data = MNTEvATive7ContextEventData(status=MNTContextStatus(data))

            if type_ == MNTEvent.DEVICE_INFO:
                self.max_contacts = data.max_contacts
                self.max_x = data.max_x
                self.max_y = data.max_y
                self.max_pressure = data.max_pressure
            elif type_ == MNTEvent.PID:
                self.pid = data.pid
            elif type_ == MNTEvent.EVATIVE7_CTX:
                if data.status == MNTContextStatus.ESTABLISHED:
                    self._connected = True
                    logger.info("socket connected")
                elif data.status == MNTContextStatus.CLOSED:
                    self._connected = False
                    logger.info("socket disconnected")

            if self._callback:
                self._callback(type_, data)
        except Exception as e:
            logger.warning("failed parse event {}: {}:".format(line, e))

    def _start_mnt(self):
        """fork a process to start minitouch on android"""
        if self._additional_param:
            additional_param = " " + " ".join(self._additional_param)
        else:
            additional_param = ""
        command_list = [
            self.adb_executor,
            "-s",
            self.device_id,
            "shell",
            self._mnt_home + additional_param,
        ]
        logger.info("start minitouch: {}".format(" ".join(command_list)))
        self.mnt_process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
        Thread(
            target=_read_std, args=(self.mnt_process, self._process_callback)
        ).start()

    def heartbeat(self):
        """check if minitouch process alive"""
        return self.mnt_process.poll() is None
