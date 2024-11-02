from .Animation import Animation

@Animation.register
class Pulse(Animation):
    def __init__(self, start, end, duration, mirror=False, *args, **kwargs):
        super().__init__(min_value=start, max_value=end)
        
        if start > end:
            raise ValueError("Start value must be less than or equal to end value.")
        
        self._mirror = mirror  # Initialize the _mirror attribute
        delay = duration / abs(end - start)
        self._duration = duration
        
        for i in range(start, end):
            self._frames.append((Animation.Command.SET.value, i))
            if duration > 0:
                self._frames.append((Animation.Command.SLEEP.value, delay))
        
        if mirror:
            self._frames += self._frames[::-1]  # Create a mirrored effect
            
    @property
    def duration(self):
        return self._duration
    
    @property
    def mirror(self):
        return self._mirror