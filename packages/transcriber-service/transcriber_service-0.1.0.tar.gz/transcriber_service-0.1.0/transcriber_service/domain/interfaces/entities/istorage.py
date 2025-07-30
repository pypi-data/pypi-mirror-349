from abc import ABC, abstractmethod


class IStorage(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @id.setter
    @abstractmethod
    def id(self, id_: str): ...

    @property
    @abstractmethod
    def user_id(self) -> str: ...

    @property
    @abstractmethod
    def audio_record_ids(self) -> list[str]: ...

    @abstractmethod
    def add_audio_record(self, record_id: str) -> None: ...

    @abstractmethod
    def remove_audio_record(self, record_id: str) -> None: ...
