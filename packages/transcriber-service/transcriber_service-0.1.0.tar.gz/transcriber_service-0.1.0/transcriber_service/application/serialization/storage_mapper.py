from .dto.storage_dto import StorageDTO
from ...domain.factories import StorageFactory, IStorageFactory
from ...domain.interfaces import IMapper, IStorage


class StorageMapper(IMapper):
    def __init__(self, factory: IStorageFactory = StorageFactory()):
        self._factory = factory

    def to_dto(self, storage: IStorage) -> StorageDTO:
        if not isinstance(storage, IStorage):
            raise TypeError("Object must be a IStorage instance")

        return StorageDTO(
            entity_type="storage",
            id=storage.id,
            user_id=storage.user_id,
            audio_record_ids=storage.audio_record_ids,
        )

    def from_dto(self, dto: StorageDTO) -> IStorage:
        storage = self._factory.create_storage(dto.user_id)
        storage.id = dto.id
        for record_id in dto.audio_record_ids:
            storage.add_audio_record(record_id)

        return storage
