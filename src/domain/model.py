from domain.errors import ResourceHandlerError, BAD_ITEM_ERROR

class ResourceType:
    id: int
    name: str
    max_speed: int

    def __init__(self, name, max_speed, id = 0):
        if name is None or max_speed is None or not isinstance(name, str) or not isinstance(max_speed, int):
            raise ResourceHandlerError(BAD_ITEM_ERROR)
        self.id = id
        self.name = name
        self.max_speed = max_speed

    def output(self):
        return {
            'id': self.id,
            'name': self.name,
            'max_speed': self.max_speed
        }

class Resource:
    id: int
    type: ResourceType
    name: str
    speed: int

    def __init__(self, type, name, speed, id = 0):
        self.id = id
        self.type = type
        self.name = name
        self.speed = speed