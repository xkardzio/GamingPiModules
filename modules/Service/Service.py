class Service:
    class HttpCodes:
        OK = 200
        BAD_REQUEST = 400
        NOT_FOUND = 404
        INTERNAL_SERVER_ERROR = 500

    def __init__(self, app, base_url, template, *args, **kwargs):
        self._app = app
        self._base_url = base_url
        self._template = template
        self.register_routes()

    @property
    def base_url(self):
        return self._base_url

    @property
    def template(self):
        return self._template

    @property
    def app(self):
        return self._app

    def register_routes(self):
        raise NotImplementedError("Subclasses should implement this method")
