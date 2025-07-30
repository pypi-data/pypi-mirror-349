from .audio_mapper import AudioRecordMapper
from .storage_mapper import StorageMapper
from .user_mapper import UserMapper
from ...domain.interfaces import IMapper


class EntityMapperFactory(object):
    def __init__(self):
        self._mappers: dict[str, IMapper] = {
            "authuser": UserMapper(),
            "admin": UserMapper(),
            "storage": StorageMapper(),
            "audiorecord": AudioRecordMapper(),
        }

    def get_mapper(self, entity_type: str) -> IMapper:
        """
        Get serializer for an entity type.

        :param entity_type: Type of the entity (e.g., 'authuser', 'storage').
        :return: IDictable serializer.
        :raises ValueError: If serializer is not found.
        """
        serializer = self._mappers.get(entity_type)
        if serializer is None:
            raise ValueError(f"No serializer found for entity type: {entity_type}")

        return serializer

    def register_mapper(self, entity_type: str, serializer: IMapper) -> None:
        """
        Register a new serializer for an entity type.

        :param entity_type: Type of the entity.
        :param serializer: Serializer implementing IDictable.
        :raises ValueError: If entity_type is invalid.
        """
        if not entity_type:
            raise ValueError(f"Entity type is invalid: {entity_type}")
        if not isinstance(serializer, IMapper):
            raise TypeError("Serializer must implement IMapper.")

        self._mappers[entity_type] = serializer
