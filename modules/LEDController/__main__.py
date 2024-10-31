from LedSerialHandler import LedSerialHandler
from Led import Led
from LedAnimations import Pulse, Blink

import time
Led.DEFAULT_MAX = 150

led_serial = LedSerialHandler(port='COM7', baudrate=115200, timeout=0)

try:
    pulse_animation = Pulse(0, Led.DEFAULT_MAX, 1000, mirror=True)

    blink_animation = Blink(1000, 1000, repeat=2)

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
    
