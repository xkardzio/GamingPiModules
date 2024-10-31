from ..KeyBinder import KeyBinder
from ..Service import Service


class KeyBinderService(KeyBinder, Service):

    def __init__(self, config=None):
        KeyBinder.__init__(self, config)
        Service.__init__(self, base_url="key-binder", template="key-binder.html")

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
