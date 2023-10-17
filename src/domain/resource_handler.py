from ports.storage import Storage
from domain.model import ResourceType

class ResourceHandlerError(Exception):
    type = 'unknown'
    def __init__(self, type, *args):
        super().__init__(args)
        self.type = type

    def __str__(self):
        return f'{self.type}'

class ResourceHandler:
    
    storage: Storage

    def __init__(self, storage):
        self.storage = storage

    def get_types(self, ids: list[int]) -> dict:
        success, items = self.storage.get_types(ids)
        if success:
            return [item.output() for item in items]
        else:
            raise ResourceHandlerError('unknown db error')

    def create_type(self, item: dict) -> dict:
        name = item.get('name', '')
        max_speed = item.get('max_speed', '')
        type = ResourceType(name, max_speed)
        success, item = self.storage.create_type(type)
        if success:
            return item.output()
        else:
            raise ResourceHandlerError('unknown db error')
    
    def delete_types(self, ids: list[int]) -> dict:
        success, items = self.storage.delete_types(ids)
        if success:
            return [item.output() for item in items]
        else:
            raise ResourceHandlerError('unknown db error')
    