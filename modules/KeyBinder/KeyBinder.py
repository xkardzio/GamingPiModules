import json
from ..Tools import PLATFORM, PlatformType
import threading

if PLATFORM == PlatformType.RPI:
    import keyboard
    from gpiozero import Button
else:
    from ..Stubs import keyboard
    from ..Stubs.gpiozero import Button
    



class Key:
    profile = "default"

    def __init__(self, GPIO_PIN, profiles):
        self._GPIO_PIN = GPIO_PIN
        self._profiles = {profile["name"]: profile["trigger"] for profile in profiles}

        self._button = Button(pin=self._GPIO_PIN, hold_time=0.02)
        self._button.when_held = self.pressed
        self._button.when_released = self.released
        self.running = False

    def __str__(self):
        key_object = {"gpio_pin": self._GPIO_PIN, "profiles": self._profiles}
        return str(key_object)

    @property
    def gpio_pin(self):
        return self._GPIO_PIN

    @gpio_pin.setter
    def gpio_pin(self, value):
        self._GPIO_PIN = value

    def pressed(self):
        try:
            keyboard.press(self._profiles[Key.profile])
        except KeyError:
            print(
                f"There isn't such key for mode {Key.profile} - key on GPIO pin {self.gpio_pin}"
            )

    def released(self):
        try:
            keyboard.release(self._profiles[Key.profile])
        except KeyError:
            print(
                f"There isn't such key for mode {Key.profile} - key on GPIO pin {self.gpio_pin}"
            )


class KeyBinder:
    def __init__(self, config=None):
        self._keys = {}
        self._profile = "default"
        self._correctPinsNumbers = [
            2,
            3,
            4,
            14,
            15,
            17,
            18,
            27,
            22,
            23,
            24,
            10,
            9,
            25,
            11,
            8,
            7,
            5,
            6,
            12,
            13,
            19,
            16,
            26,
            20,
            21,
        ]

        if config is not None:
            if isinstance(config, str):
                config = json.loads(config)
            self.load_config(config)
        Key.profile = self._profile
        self.running = False  # Initialize running flag

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value
        Key.profile = value

    def load_config(self, config):
        if self._keys:
            self.delete_config()
            
        used_pins = []

        if isinstance(config, str):
            config = json.loads(config)

        for key_info in config.get("KeyConfig", []):
            if "gpio_pin" not in key_info:
                raise ValueError("Missing 'gpio_pin' in key configuration.")

            gpio_pin = key_info["gpio_pin"]

            if gpio_pin not in self._correctPinsNumbers:
                raise ValueError(f"Invalid GPIO pin: {gpio_pin}")

            if gpio_pin in used_pins:
                raise ValueError(f"GPIO pin {gpio_pin} is already used.")

            used_pins.append(gpio_pin)

            if "profiles" not in key_info:
                raise ValueError(f"Missing 'profiles' for GPIO pin: {gpio_pin}")

            profiles = key_info["profiles"]

            self._keys[gpio_pin] = Key(gpio_pin, profiles)

        return True

    def get_config(self):
        keys_info = []
        for gpio_pin, key in self._keys.items():
            profiles_info = [
                {"name": profile_name, "trigger": trigger}
                for profile_name, trigger in key._profiles.items()
            ]
            keys_info.append({"gpio_pin": gpio_pin, "profiles": profiles_info})

        return keys_info

    def delete_config(self):
        for key in self._keys.values():
            key.released()
            key._button.close()
            
        self._keys = {}
    
    def run(self):
        def loop():
            while self.running:
                pass

        thread = threading.Thread(target=loop)
        self.running = True
        thread.start()

    def stop(self):
        self.running = False
