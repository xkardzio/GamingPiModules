from ..KeyBinder import KeyBinder
from ..Service import Service

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
            try:
                KeyBinder.load_config(self, config)
                return {"message": "Config loaded successfully"}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.BAD_REQUEST

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/config", methods=["GET"])
        def get_config():
            try:
                return {"KeyConfig" : KeyBinder.get_config(self)}, self.HttpCodes.OK
            except Exception as e:
                return {"error": str(e)}, self.HttpCodes.INTERNAL_SERVER_ERROR

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/profile", methods=["POST"])
        def change_profile():
            try:
                profile = request.json["profile"]
            except KeyError:
                return {"error": "Field 'profile' is required"}, self.HttpCodes.BAD_REQUEST
                
            KeyBinder.profile.fset(self, profile)
            return {"message": "Profile changed successfully"}, self.HttpCodes.OK

        @self.app.route(f"{self.base_url}/{self.MODULE_URL}/profile", methods=["GET"])
        def get_profile():
            return {"profile": KeyBinder.profile.fget(self)}, self.HttpCodes.OK

