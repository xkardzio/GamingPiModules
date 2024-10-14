class Service:
    class HttpCodes:
        OK = 200
        BAD_REQUEST = 400
        NOT_FOUND = 404
        INTERNAL_SERVER_ERROR = 500

    def __init__(self, base_url, template):
        self._base_url = base_url
        self._template = template

    @property
    def base_url(self):
        return self._base_url

    @property
    def template(self):
        return self._template
