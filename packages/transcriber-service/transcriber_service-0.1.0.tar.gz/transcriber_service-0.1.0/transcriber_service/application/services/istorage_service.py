from abc import ABC, abstractmethod

from ...domain.interfaces import IStorage


class IStorageService(ABC):
    @abstractmethod
    def create_storage(self, user_id: str) -> IStorage: ...

    @abstractmethod
    def get_user_storage(self, user_id: str) -> IStorage | None: ...

    @abstractmethod
    def remove_audio_record(self, storage_id: str, record_id: str) -> None: ...

    @abstractmethod
    def get_all_record_ids(self, storage_id: str) -> list[str] | None: ...
