from ports.storage import Storage
from domain.model import ResourceType
from domain.errors import ResourceHandlerError, UNKNOWN_DB_ERROR

class ResourceHandler:
    
    storage: Storage

    def __init__(self, storage):
        self.storage = storage

    def create_type(self, item: dict) -> dict:
        name = item.get('name', None)
        max_speed = item.get('max_speed', None)
        type = ResourceType(name, max_speed)
        success, item = self.storage.create_type(type)
        if success:
            return item.output()
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        
    def update_type(self, id: int, item: dict) -> dict:
        success, [dbitem] = self.storage.get_types([id])
        if not success:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        name = item.get('name', dbitem.name)
        max_speed = item.get('max_speed', dbitem.max_speed)
        type = ResourceType(name, max_speed, id)
        success, item = self.storage.update_type(type)
        if success:
            return item.output()
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)

    def get_types(self, ids: list[int]) -> dict:
        success, items = self.storage.get_types(ids)
        if success:
            return [item.output() for item in items]
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
    
    def delete_types(self, ids: list[int]) -> dict:
        success, items = self.storage.delete_types(ids)
        if success:
            return [item.output() for item in items]
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
