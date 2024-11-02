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
            Led.serialHandler = self._led_serial_handler

    def register_routes(self):

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}", methods=["GET"])
        def LEDController_page():
            return render_template(f"{self.MODULE_URL}/{self.template}")

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/leds", methods=["GET"])
        def get_leds():
            return get_function_result(self.leds)

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/leds/add", methods=["POST"])
        def add_leds():
            return get_function_result(self.add_leds(request.json))

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/leds", methods=["POST"])
        def update_leds():
            print(request.json)
            try:
                pins = request.json.get("pins", [])
                newConfig = request.json.get("newConfig", {})
                if not isinstance(pins, list):
                    raise ValueError("Expected 'pins' to be a list.")
                for pin in pins:
                    led = self._led_serial_handler.leds.get(pin)
                    if led is None:
                        raise ValueError(f"LED with pin {pin} not found.")
                    led.update(**newConfig)
                return {"message": "LEDs updated successfully"}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST
                    
        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_id>",
            methods=["GET"],
        )
        def get_led(led_id):
            try:
                led = self._led_serial_handler.leds.get(led_id)
                return {"led": led.to_json()}, self.HttpCodes.OK
            except Exception as e:
                return self.HttpCodes.INTERNAL_SERVER_ERROR, str(e)   

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_id>",
            methods=["post"],
        )
        def update_led(led_id):
            return get_function_result(self.update_led(led_id, request.json))
        
        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_id>/animation",
            methods=["GET"],
        )
        def get_led_animation(led_id):
            try:
                led_animation = self._led_serial_handler.leds.get(led_id).animation
                led_animation = led_animation.to_json() if led_animation is not None else {}
                return {"animation": {led_animation}}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_id>/animation",
            methods=["post"],
        )
        def update_led_animation(led_id):
            return get_function_result(self.update_led(led_id, {"animation":request.json}))

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/led-serial-handler/running",
            methods=["GET"],
        )
        def get_led_serial_handler_running():
            return get_function_result(self._led_serial_handler.running)

    def add_leds(self, data):
        try:
            leds = data.get("leds", [])
            if not isinstance(leds, list):
                raise ValueError("Expected 'leds' to be a list.")

            for led in leds:
                self._led_serial_handler.add_led(Led.from_json(led))
            return self.HttpCodes.OK
        except Exception as e:
            return self.HttpCodes.BAD_REQUEST, str(e)

    @property
    def leds(self):
        if self._led_serial_handler is not None:
            serialized_leds = []
            for led in self._led_serial_handler.leds.values():
                serialized_leds.append(led.to_json())
            return self.HttpCodes.OK, {"leds": serialized_leds}
        else:
            return (
                self.HttpCodes.INTERNAL_SERVER_ERROR,
                "LED Serial Handler not initialized",
            )
            
    def led(self, led_id):
        led = self._led_serial_handler.leds.get(led_id)
        if led is None:
            return self.HttpCodes.NOT_FOUND, f"LED with id {led_id} not found."
        return self.HttpCodes.OK, led.to_json()

    def update_led(self, led_id, data):
        try:
            led = self._led_serial_handler.leds.get(led_id)
            if led is None:
                raise ValueError(f"LED with id {led_id} not found.")
            led.update(**data)
            return self.HttpCodes.OK
        except Exception as e:
            return self.HttpCodes.BAD_REQUEST, str(e)
