from .istorage_service import IStorageService
from ..serialization import StorageMapper, StorageDTO
from ...domain.factories import IStorageFactory, StorageFactory
from ...domain.interfaces import IStorageRepository


class StorageService(IStorageService):
    """Manages storage creation and retrieval."""

    def __init__(self, storage_repo: IStorageRepository):
        self.__storage_repository = storage_repo
        self.__storage_factory: IStorageFactory = StorageFactory()
        self.mapper = StorageMapper()

    def create_storage(self, user_id: str) -> StorageDTO:
        """Creates a new storage container for a user."""

        storage = self.__storage_factory.create_storage(user_id)
        self.__storage_repository.add(storage)
        return self.mapper.to_dto(storage)

    def get_user_storage(self, user_id: str) -> StorageDTO:
        """Returns storage by user id if it exists else None."""

        storage = self.__storage_repository.get_by_user(user_id)
        return self.mapper.to_dto(storage)

    def remove_audio_record(self, storage_id: str, record_id: str) -> None:
        storage = self.__storage_repository.get_by_id(storage_id)
        storage.remove_audio_record(record_id)
        self.__storage_repository.update(storage)

    def get_all_record_ids(self, storage_id: str) -> list[str] | None:
        storage = self.__storage_repository.get_by_id(storage_id)
        return storage.audio_record_ids if storage else []
