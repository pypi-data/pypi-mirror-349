from typing import Any

from pydantic import BaseModel

from .dto import UserDTO, StorageDTO, AudioRecordDTO
from .entity_mapper_factory import EntityMapperFactory
from ...domain.interfaces import ISerializer


class SerializerAdapter(ISerializer):
    def __init__(
        self,
        base_serializer: ISerializer,
        entity_mapper_factory: EntityMapperFactory,
    ):
        self._base_serializer = base_serializer
        self._entity_mapper_factory = entity_mapper_factory
        self._dto_mapping = {
            "authuser": UserDTO,
            "admin": UserDTO,
            "storage": StorageDTO,
            "audiorecord": AudioRecordDTO,
        }

    def serialize(self, obj) -> str | bytes:
        """
        Serialize data, converting entities to DTOs.

        :param obj: Data to serialize (entity or DTO).
        :return: Serialized data (string or bytes).
        """

        data = self._to_dto(obj)
        return self._base_serializer.serialize(data)

    def deserialize(self, data: str | bytes):
        """
        Deserialize data, restoring entities from DTOs.

        :param data: Serialized data.
        :return: Deserialized data (entities or DTOs).
        """

        deserialized = self._base_serializer.deserialize(data)
        return self._from_dto(deserialized)

    def _to_dto(self, obj):
        """Convert an entity to a DTO if applicable."""

        if isinstance(obj, BaseModel):
            return obj.model_dump()
        if isinstance(obj, (list, tuple, set)):
            return [self._to_dto(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._to_dto(value) for key, value in obj.items()}
        elif (
            hasattr(obj, "__class__")
            and obj.__class__.__name__.lower() in self._dto_mapping
        ):
            serializer = self._entity_mapper_factory.get_mapper(
                obj.__class__.__name__.lower()
            )
            return serializer.to_dto(obj).model_dump()
        return obj

    def _from_dto(self, data: Any) -> Any:
        """Restore an entity from a DTO if applicable."""
        if isinstance(data, (list, tuple)):
            return [self._from_dto(item) for item in data]
        elif isinstance(data, dict) and "entity_type" in data:
            dto_class = self._dto_mapping.get(data["entity_type"])
            if dto_class:
                dto = dto_class(**data)
                serializer = self._entity_mapper_factory.get_mapper(data["entity_type"])
                return serializer.from_dto(dto)
        elif isinstance(data, dict):
            return {key: self._from_dto(value) for key, value in data.items()}
        return data

    @property
    def extension(self) -> str:
        return self._base_serializer.extension

    @property
    def binary(self) -> bool:
        return self._base_serializer.binary
