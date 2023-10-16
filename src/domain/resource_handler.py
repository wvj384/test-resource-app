from ports.storage import Storage
from domain.model import ResourceType

class ResourceHandler:
    
    storage: Storage

    def __init__(self, storage):
        self.storage = storage

    def get_type(self, params:dict) -> dict:
        ids = params.get('ids', [])
        success, items = self.storage.get_types(ids)
        if success:
            return [item.__dict__ for item in items] # FIXME looks not good
        else:
            return {'error':'db error'}

    def create_type(self, item):
        name = item.get('name', '')
        max_speed = item.get('max_speed', '')
        type = ResourceType(name, max_speed)
        success, item = self.storage.create_type(type)
        print(success)
        print(item.__dict__)
        if success:
            return item.__dict__
        else:
            return {'error':'db error'}

    def update_type(self, params, object):
        return True
    
    def delete_type(self, params):
        return True

    def get_resource(self, params):
        return {"name":"resource1", "type":"type1", "speed":90}
    
    def create_resource(self, object):
        return True

    def update_resource(self, params, object):
        return True
    
    def delete_resource(self, params):
        return True
    
    