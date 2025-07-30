from abc import ABC, abstractmethod
from typing import Any


class ISerializer(ABC):
    @abstractmethod
    def serialize(self, data: Any) -> str | bytes: ...

    @abstractmethod
    def deserialize(self, data: str | bytes) -> Any: ...

    @property
    @abstractmethod
    def binary(self) -> bool: ...

    @property
    @abstractmethod
    def extension(self) -> str: ...
