from abc import ABC, abstractmethod
from datetime import datetime


class IAudioRecord(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @id.setter
    @abstractmethod
    def id(self, id_: str): ...

    @property
    @abstractmethod
    def text(self) -> str: ...

    @text.setter
    @abstractmethod
    def text(self, value: str) -> None: ...

    @property
    @abstractmethod
    def language(self) -> str: ...

    @property
    @abstractmethod
    def tags(self) -> list: ...

    @abstractmethod
    def add_tag(self, tag_name: str, update: bool = True) -> None: ...

    @abstractmethod
    def remove_tag(self, tag_name: str) -> None: ...

    @property
    @abstractmethod
    def record_name(self) -> str: ...

    @record_name.setter
    @abstractmethod
    def record_name(self, note_name: str): ...

    @property
    @abstractmethod
    def storage_id(self) -> str: ...

    @property
    @abstractmethod
    def file_path(self) -> str: ...

    @property
    @abstractmethod
    def last_updated(self) -> datetime: ...

    @last_updated.setter
    @abstractmethod
    def last_updated(self, value: datetime): ...
