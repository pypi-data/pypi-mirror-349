from abc import ABC, abstractmethod

from ..entities.storage import Storage
from ..interfaces import IStorage


class IStorageFactory(ABC):

    @abstractmethod
    def create_storage(self, user_id: str) -> IStorage:
        pass


class StorageFactory(IStorageFactory):

    def create_storage(self, user_id: str) -> IStorage:
        return Storage(user_id)
