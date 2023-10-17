from ports.storage import Storage
from domain.model import ResourceType, Resource
from domain.errors import ResourceHandlerError, UNKNOWN_DB_ERROR, INVALID_TYPE_ERROR, INVALID_ID_ERROR

class ResourceHandler:
    
    storage: Storage

    def __init__(self, storage):
        self.storage = storage

    # Types

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
        success, dbitem = self.storage.get_types([id])
        if not success:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        if len(dbitem) == 0:
            raise ResourceHandlerError(INVALID_ID_ERROR)
        oldtype = dbitem[0]
        name = item.get('name', oldtype.name)
        max_speed = item.get('max_speed', oldtype.max_speed)
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
        
    # Resources

    def create_resource(self, item: dict) -> dict:
        name = item.get('name', None)
        type_id = item.get('type_id', None)
        speed = item.get('speed', None)
        success, dbtypes = self.storage.get_types([type_id])
        if not success:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        if len(dbtypes) == 0:
            raise ResourceHandlerError(INVALID_TYPE_ERROR)
        resource = Resource(name, dbtypes[0], speed)
        success, item = self.storage.create_resource(resource)
        if success:
            return item.output()
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        
    def update_resource(self, id: int, item: dict) -> dict:
        success, dbitem = self.storage.get_resources([id])
        if not success:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        if len(dbitem) == 0:
            raise ResourceHandlerError(INVALID_ID_ERROR)
        olditem = dbitem[0]
        name = item.get('name', olditem.name)
        speed = item.get('speed', olditem.speed)
        type_id = item.get('type_id', olditem.type.id)
        type = olditem.type
        if type_id != olditem.type.id:
            success, dbtype = self.storage.get_types([type_id])
            if not success:
                raise ResourceHandlerError(UNKNOWN_DB_ERROR)
            if len(dbtype) == 0:
                raise ResourceHandlerError(INVALID_TYPE_ERROR)
            type = dbtype[0]
        resource = Resource(name, type, speed, id)
        success, item = self.storage.update_resource(resource)
        if success:
            return item.output()
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)

    def get_resources(self, ids: list[int]) -> dict:
        success, items = self.storage.get_resources(ids)
        if success:
            return [item.output() for item in items]
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)
        
    def delete_resources(self, ids: list[int]) -> dict:
        success, items = self.storage.delete_resources(ids)
        if success:
            return [item.output() for item in items]
        else:
            raise ResourceHandlerError(UNKNOWN_DB_ERROR)