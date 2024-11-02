from ..Service import Service

from flask import render_template


class MainService(Service):

    def __init__(self, base_url="/launcher-api", template="base.html", *args, **kwargs):
        Service.__init__(self, base_url=base_url, template=template, *args, **kwargs)

    def register_routes(self):
        @self.app.route(f"{self.base_url}/", methods=["GET"])
        @self.app.route(f"/", methods=["GET"])
        def API_page():
            return render_template(self.template)
