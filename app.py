from adapters.wsgi import WsgiApp
from domain.resource_handler import ResourceHandler

resource_handler = ResourceHandler()
app = WsgiApp(resource_handler)
