from LedSerialHandler import LedSerialHandler
from Led import Led
from LedAnimations import Pulse, Blink, Animation
import json

import time
Led.DEFAULT_MAX = 50
LED_PORT = '/dev/ttyUSB0' # Shall be changed to the correct port. Prefered stored as a environment variable
try:
    led_serial = LedSerialHandler(port=LED_PORT, baudrate=115200, timeout=0)
except Exception as e:
    print(e)
    exit()
    
pulse_json = {
    "animationType": "Pulse",
    "start": 0,
    "end": Led.DEFAULT_MAX,
    "duration": 500,
    "mirror": True,
}

try:
    pulse_animation = Animation.from_json(json.dumps(pulse_json))

    led = Led(3, led_serial)
    led5 = Led(5, led_serial)
    led6 = Led(6, led_serial)
    led9 = Led(9, led_serial)
    led10 = Led(10, led_serial)
    led11 = Led(11, led_serial)

    leds = [led, led5, led6, led9, led10, led11]
    group1 = [led, led9]
    group2 = [led5, led10]
    group3 = [led6, led11]

    for led in leds:
        led.animation_loop = True
    
    for led in group1:
        led.animation = pulse_animation
    
    for led in group2:
        led.animation = pulse_animation
        led.animation_delay = pulse_animation.duration / 2
        
    for led in group3:
        led.animation = pulse_animation
        led.animation_delay = pulse_animation.duration
        
    for ledi in leds:
        led_serial.add_led(ledi)
        
    time.sleep(LedSerialHandler.INIT_TIME)
    input("Led serial handler initialized")
    
    for ledi in led_serial.leds.values():
        ledi.animation_running = True
        
    input("Press")
    led_serial.close()
except KeyboardInterrupt:
    led_serial.close()
    
