from ..KeyBinder import KeyBinder

class KeyBinderService(KeyBinder):
    BASE_URL = 'key-binder'
    def __init__(self, config=None):
        super().__init__(config)