from abc import ABC, abstractmethod

from domain.model import ResourceType, Resource

class Storage(ABC):
    
    @abstractmethod
    def get_types(self, ids: [int]) -> (bool, list[ResourceType] | None):
        pass
    
    @abstractmethod
    def create_type(self, item: ResourceType) -> (bool, ResourceType | None):
        pass