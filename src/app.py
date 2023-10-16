from adapters.wsgi import WsgiApp
from adapters.postgres import PostgresStorage
from domain.resource_handler import ResourceHandler

storage = PostgresStorage(host='127.0.0.1', port=5432, dbname='resourcedb', user='postgres', password='qwerty')
resource_handler = ResourceHandler(storage)
app = WsgiApp(resource_handler)
