from ..KeyBinder import KeyBinder
from ..Service import Service
from ..Tools import get_function_result

from flask import render_template, request


class KeyBinderService(KeyBinder, Service):
    MODULE_URL = "key-binder"

    def __init__(self, config=None, *args, **kwargs):
        KeyBinder.__init__(self, config)
        Service.__init__(self, *args, **kwargs)

    def register_routes(self):

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}", methods=["GET"])
        def KeyBinder_page():
            return render_template(f"{self.MODULE_URL}/{self.template}")

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/config", methods=["POST"])
        def load_config():
            config = request.json
            return get_function_result(self.load_config(config))

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/config", methods=["GET"])
        def get_config():
            return get_function_result(self.get_config())

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/profile", methods=["POST"])
        def change_profile():
            self.profile = request.json
            return get_function_result(self.profile)

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/profile", methods=["GET"])
        def get_profile():
            return get_function_result(self.profile)

    def load_config(self, config):
        try:
            KeyBinder.load_config(self, config)
            return self.HttpCodes.OK
        except Exception as e:
            return self.HttpCodes.BAD_REQUEST, str(e)

    def get_config(self):
        return self.HttpCodes.OK, {"KeyConfig": super().get_config()}

    @property
    def profile(self):
        return self.HttpCodes.OK, KeyBinder.profile.fget(self)

    @profile.setter
    def profile(self, value):
        KeyBinder.profile.fset(self, value)
        return self.HttpCodes.OK
