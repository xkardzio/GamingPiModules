from ..LEDController import LedSerialHandler, Led
from ..LEDController.LedAnimations import Animation

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
            if self._led_serial_handler is None:
                return {"error": "LED serial handler not found."}, self.HttpCodes.INTERNAL_SERVER_ERROR
            try:
                leds = [led.to_json() for led in self._led_serial_handler.leds.values()]
                return {"leds": leds}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.INTERNAL_SERVER_ERROR
                

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/leds/add", methods=["POST"])
        def add_leds():
            try:
                self.add_leds(request.json)
                return {"message": "LEDs added successfully"}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/leds", methods=["POST"])
        def update_leds():
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
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_pin>",
            methods=["GET"],
        )
        def get_led(led_pin):
            try:
                led = self._led_serial_handler.leds.get(led_pin)
                if led is None:
                    raise KeyError
                return {"led": led.to_json()}, self.HttpCodes.OK
            except KeyError :
                return {"error": f"LED with pin {led_pin} not found."}, self.HttpCodes.NOT_FOUND
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_pin>",
            methods=["POST"],
        )
        def update_led(led_pin):
            try:
                led = self._led_serial_handler.leds.get(led_pin)
                if led is None:
                    raise KeyError
                led.update(**request.json)
                return {"message": "LED updated successfully"}, self.HttpCodes.OK
            except KeyError:
                return {"error": f"LED with pin {led_pin} not found."}, self.HttpCodes.NOT_FOUND
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_pin>/animation",
            methods=["GET"],
        )
        def get_led_animation(led_pin):
            try:
                led_animation = self._led_serial_handler.leds.get(led_pin).animation
                led_animation = (
                    led_animation.to_json() if led_animation is not None else {}
                )
                return {"animation": {led_animation}}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/leds/<int:led_pin>/animation",
            methods=["post"],
        )
        def update_led_animation(led_pin):
            try:
                led = self._led_serial_handler.leds.get(led_pin)
                if led is None:
                    raise KeyError
                animation = request.json.get("animation")
                if animation is None:
                    raise ValueError("Field 'animation' is required.")
                led.animation = Animation.from_json(animation)
                return {"message": "Animation updated successfully"}, self.HttpCodes.OK
            except KeyError as e:
                return {"error": f"LED with id {led_pin} not found."}, self.HttpCodes.NOT_FOUND
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(
            f"{self.base_url}/{self.MODULE_URL}/led-serial-handler/running",
            methods=["GET"],
        )
        def get_led_serial_handler_running():
            try:
                return {"running": self._led_serial_handler.running}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.INTERNAL_SERVER_ERROR

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