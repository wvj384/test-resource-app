from abc import ABC, abstractmethod

from domain.model import ResourceType, Resource

class Storage(ABC):
    
    @abstractmethod
    def create_type(self, item: ResourceType) -> (bool, ResourceType | None):
        pass

    @abstractmethod
    def update_type(self, item: ResourceType) -> (bool, ResourceType | None):
        pass

    @abstractmethod
    def get_types(self, ids: [int]) -> (bool, list[ResourceType] | None):
        pass

    @abstractmethod
    def delete_types(self, ids: [int]) -> (bool, ResourceType | None):
        pass

    @abstractmethod
    def create_resource(self, item: Resource) -> (bool, Resource | None):
        pass

    @abstractmethod
    def update_resource(self, item: Resource) -> (bool, Resource | None):
        pass
    
    @abstractmethod
    def get_resources(self, ids: [int], type_ids: [int]) -> (bool, list[Resource] | None):
        pass

    @abstractmethod
    def delete_resources(self, ids: [int]) -> (bool, Resource | None):
        pass