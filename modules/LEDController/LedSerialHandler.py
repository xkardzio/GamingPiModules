import serial 
import threading
import queue
import time
from enum import Enum

class LedSerialHandler:
    
    INIT_TIME = 3
    
    class Response(Enum):
        COMMAND_ERROR = 0x64
        COMMAND_SUCCESS = 0x65
        INIT_ERROR = 0x6e
        INIT_SUCCESS = 0x6f
        PIN_ERROR = 0xc8
        PIN_OK = 0xc9
        
    class Command(Enum):
        INIT = 0x32
    
    def __init__(self, port, baudrate=9600, timeout=0, init_time = INIT_TIME):
        self.serial_port = None
        
        init_thread = threading.Thread(target=self.serial_init, args=(port, baudrate, timeout, init_time))
        init_thread.start()
        
        self.queue = queue.Queue()
        self.running = True
        
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.start()
        
        self._leds = {}
    
    def init(self):
        message = bytes([self.Command.INIT.value, 0x0])
        response_queue = self.send(message, read_bytes_count=1)
        response = response_queue.get()
        
        if int.from_bytes(response, byteorder='little') == LedSerialHandler.Response.INIT_SUCCESS.value:
            return True
        else:
            return False
        
    def serial_init(self, port, baudrate=9600, timeout=0, init_time=INIT_TIME):
        if self.serial_port is not None:
            raise Exception('Serial port already initialized')
        
        self.serial_port = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(init_time)
        self.serial_port.reset_input_buffer()
        
        if not self.init():
            raise Exception('Error initializing serial port')
    
    def send(self, message, read_bytes_count=0):
        response_queue = queue.Queue()
        self.queue.put((message, read_bytes_count, response_queue))
        return response_queue
    
    def _process_queue(self):
        while self.running or not self.queue.empty():
            try:
                if self.serial_port is not None:
                    message, read_bytes_count, response_queue = self.queue.get(timeout=0)
                    self.serial_port.write(message)
                    
                    response = b''
                    if read_bytes_count > 0:
                        while len(response) < read_bytes_count:
                            response += self.serial_port.read(read_bytes_count - len(response))
                        response_queue.put(response)
                    
                    self.queue.task_done()
            except queue.Empty:
                pass
        
    
    def close(self):
        self.running = False
        
        for led in self.leds.values():
            led.animation_running = False
            
        self.queue.join()
        self.thread.join()
            
        if self.serial_port.is_open:
            self.serial_port.close()
            self.serial_port = None

    def add_led(self, led):
        self._leds[led.pin] = led
        
    @property
    def leds(self):
        return self._leds