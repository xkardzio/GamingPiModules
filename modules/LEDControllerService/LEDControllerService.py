from ..LEDController import LedSerialHandler, Led
from ..LEDController.LedAnimations import Animation

from ..Tools import get_function_result
from ..Service import Service

from flask import render_template, request


class LEDControllerService(Service):
    MODULE_URL = "led-controller"

    def __init__(self, *args, **kwargs):
        Service.__init__(self, *args, **kwargs)

        if "led_serial_handler" in kwargs:
            self._led_serial_handler = kwargs["led_serial_handler"]

    def register_routes(self):

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}", methods=["GET"])
        def LEDController_page():
            return render_template(f"{self.MODULE_URL}/{self.template}")

    @property
    def leds(self):
        if self._led_serial_handler is not None:
            return self.HttpCodes.OK, self._led_serial_handler.leds
        else:
            return (
                self.HttpCodes.INTERNAL_SERVER_ERROR,
                "LED Serial Handler not initialized",
            )
