from adapters.postgres import PostgresStorage
from domain.wsgi import WsgiApp
from domain.resource_handler import ResourceHandler
from configparser import ConfigParser


def read_config():
    config = ConfigParser()
    config.read("config.ini")
    data = {}
    data["db_host"] = config["db"].get("host", "")
    data["db_port"] = int(config["db"].get("port", ""))
    data["db_name"] = config["db"].get("database", "")
    data["db_user"] = config["db"].get("user", "")
    data["db_pwd"] = config["db"].get("password", "")
    return data


config = read_config()

storage = PostgresStorage(
    host=config["db_host"],
    port=config["db_port"],
    dbname=config["db_name"],
    user=config["db_user"],
    password=config["db_pwd"],
)
resource_handler = ResourceHandler(storage)
app = WsgiApp(resource_handler)
