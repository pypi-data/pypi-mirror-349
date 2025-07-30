from abc import ABC, abstractmethod


class IFileManager(ABC):
    @staticmethod
    @abstractmethod
    def save(data, path: str, serializer) -> None: ...

    @staticmethod
    @abstractmethod
    def load(path: str, serializer): ...
