from .Animation import Animation

class Pulse(Animation):
    def __init__(self, start, end, duration, mirror=False):
        super().__init__(min_value=start, max_value=end)
        delay = duration / abs(end - start)
        if mirror:
            delay /= 2
        
        self._duration = duration
        
        for i in range(start, end):
            self._frames.append((Animation.Command.SET.value, i))
            if duration > 0:
                self._frames.append((Animation.Command.SLEEP.value, delay))
        
        if mirror:
            self._frames += self._frames[::-1]
            
    @property
    def duration(self):
        return self._duration
    
    @property
    def mirror(self):
        return self._mirror