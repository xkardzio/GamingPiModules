from enum import Enum
import platform
from flask import jsonify


class PlatformType(Enum):
    UNKNOWN = 0
    WINDOWS = 1
    LINUX = 2
    MAC = 3
    RPI = 4


def get_platform() -> PlatformType:
    system = platform.system()
    if system == "Windows":
        return PlatformType.WINDOWS
    elif system == "Darwin":
        return PlatformType.MAC
    elif system == "Linux":
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read()
            if "Raspberry Pi" in cpuinfo:
                return PlatformType.RPI
            else:
                return PlatformType.LINUX
    else:
        return PlatformType.UNKNOWN


def get_function_result(result):
    if isinstance(result, tuple):
        status_code, message = result
        if isinstance(message, dict):
            return {"status": status_code, **message}
        return jsonify({"status": status_code, "message": message})
    else:
        return jsonify({"status": result})


PLATFORM = get_platform()
