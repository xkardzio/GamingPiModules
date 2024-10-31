import threading
import time
from LedSerialHandler import LedSerialHandler
from LedAnimations import Animation

class Led:
    serialHandler = None
    DEFAULT_MIN = 0
    DEFAULT_MAX = 255

    def __init__(self, pin, serialHandler=None, min_value=None, max_value=None, scale_animation=True):
        self.pin = pin
        self._value = 0
        self._min = min_value if min_value is not None else Led.DEFAULT_MIN
        self._max = max_value if max_value is not None else Led.DEFAULT_MAX
        
        self._animation = None
        self._animation_running = False
        self._animation_thread = None
        self._animation_loop = False
        self._animation_delay = 0
        self._stop_event = threading.Event()
        self._current_frame = None
        self._scale_animation = scale_animation
        
        if Led.serialHandler is None:
            Led.serialHandler = serialHandler
    
    @property
    def animation_running(self):
        return self._animation_running

    @animation_running.setter
    def animation_running(self, value):
        if value and not self._animation_running:
            self._animation_running = True
            self._stop_event.clear()  
            self._animation_thread = threading.Thread(target=self._process_animation)
            self._animation_thread.start()
            
        elif not value and self._animation_running:
            self._animation_running = False
            self._stop_event.set()  
            if self._animation_thread is not None:
                try:
                    self._animation_thread.join()
                except RuntimeError:
                    # Thread already joined
                    pass
                self._animation_thread = None
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if Led.serialHandler and Led.serialHandler.running:
            message = bytes([self.pin, value])
            response_queue = Led.serialHandler.send(message, read_bytes_count=1)
            response = response_queue.get()
            if int.from_bytes(response) == LedSerialHandler.Response.PIN_OK.value:
                self._value = value
            else:
                raise Exception(f'Error setting value for pin {self.pin} - response: {LedSerialHandler.Response(response)}')
    
    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, value):
        self._min = value
    
    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, value):
        self._max = value
        
    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, animation):
        self._animation = animation
        self._animation_running = False
        self._current_frame = None
        self._animation_delay = 0

    @property
    def animation_loop(self):
        return self._animation_loop
    
    @animation_loop.setter
    def animation_loop(self, value):
        self._animation_loop = value
    
    @property
    def animation_delay(self):
        return self._animation_delay
    
    @animation_delay.setter
    def animation_delay(self, value):
        self._animation_delay = max(0,value)
    
    def _process_animation(self):
        if self.animation is None:
            return
        if self._animation_delay > 0:
            time.sleep(self._animation_delay / 1000)
        while not self._stop_event.is_set():
                
            for frame in self.animation.frames:
                if self._stop_event.is_set():
                    return

                command, value = frame
                value = round(value)
                if command == Animation.Command.SET.value:
                    if self._scale_animation:
                        self.value = int(
                            (value - self.animation.min_value) / (self.animation.max_value - self.animation.min_value)
                            * (self.max - self.min) + self.min
                        )
                    else:
                        self.value = value
                    self._current_frame = frame
                elif command == Animation.Command.SLEEP.value:
                    end_time = time.time() + (value / 1000)
                    while time.time() < end_time:
                        if self._stop_event.is_set():
                            return

            if not self.animation_loop:
                self.animation_running = False
                break