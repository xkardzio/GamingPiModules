from .Animation import Animation

class Blink(Animation):
    def __init__(self, on_duration, off_duration=None, on_value = 255, off_value = 0, repeat = 1):
        super().__init__(min_value=off_value, max_value=on_value)
        
        off_duration = off_duration if off_duration is not None else on_duration
        
        for i in range(repeat):
            self._frames.append((Animation.Command.SET.value, on_value))
            self._frames.append((Animation.Command.SLEEP.value, on_duration))
            self._frames.append((Animation.Command.SET.value, off_value))
            self._frames.append((Animation.Command.SLEEP.value, off_duration))
            
            
        
            