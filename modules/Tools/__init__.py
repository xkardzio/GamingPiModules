from enum import Enum
import platform

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
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo:
                return PlatformType.RPI
            else:
                return PlatformType.LINUX
    else:
        return PlatformType.UNKNOWN
    
PLATFORM = get_platform()
