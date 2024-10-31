from enum import Enum

class Animation:
    class Command(Enum):
        SLEEP = 0x0
        SET = 0x1
        
    def __init__(self, min_value, max_value):
        self._frames = []
        self._min_value = min_value
        self._max_value = max_value
    
    @property
    def frames(self):
        return self._frames    
    
    @property
    def min_value(self):
        return self._min_value
    
    @property
    def max_value(self):
        return self._max_value