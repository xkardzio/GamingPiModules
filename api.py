from modules import (
    MainService,
    KeyBinderService,
    LEDControllerService,
    get_function_result,
)
from modules.LEDController import LedSerialHandler

from flask import Flask, request, render_template
import os

BASE_URL = "/launcher-api"
app = Flask(__name__)

apiService = MainService(app=app, base_url=BASE_URL, template="base.html")
kb = KeyBinderService(app=app, base_url=BASE_URL, template="key-binder.html")

led_serial_port = os.environ.get("LED_SERIAL_PORT")

if led_serial_port is None:
    led_serial_port = input("Enter the serial port for the LED controller: ")

if led_serial_port is not None:
    led_serial_handler = LedSerialHandler(led_serial_port, baudrate=115200)
else:
    led_serial_handler = None

ledc = LEDControllerService(
    app=app,
    base_url=BASE_URL,
    template="led-controller.html",
    led_serial_handler=led_serial_handler,
)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)