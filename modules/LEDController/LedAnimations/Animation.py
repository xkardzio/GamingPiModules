from enum import Enum
import json

ANIMATION_CLASSES = {}

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
    
    def to_json(self):
        def serialize(obj):
            if isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            return obj

        data = {k.lstrip('_'): serialize(v) for k, v in self.__dict__.items()}
        return json.dumps(data, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        
        animation_type = data.pop("animationType", None)
        
        if animation_type not in ANIMATION_CLASSES:
            raise ValueError(f"Unknown animation type: {animation_type}")
        return ANIMATION_CLASSES[animation_type](**data)
    
    @classmethod
    def register(cls):
        ANIMATION_CLASSES[cls.__name__] = cls
        return cls
