from abc import ABC, abstractmethod

from ..entities.iaudio import IAudioRecord
from ..entities.istorage import IStorage
from ..entities.iuser import IUser


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> IUser | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> IUser | None: ...

    @abstractmethod
    def add(self, user: IUser) -> None: ...

    @abstractmethod
    def update(self, user: IUser) -> None: ...

    @abstractmethod
    def delete(self, user: IUser): ...

    @abstractmethod
    def get_all(self) -> list[IUser]: ...


class IStorageRepository(ABC):
    @abstractmethod
    def get_by_id(self, storage_id: str) -> IStorage | None: ...

    @abstractmethod
    def get_by_user(self, user_id: str) -> IStorage: ...

    @abstractmethod
    def add(self, storage: IStorage) -> None: ...

    @abstractmethod
    def update(self, storage: IStorage) -> None: ...

    @abstractmethod
    def delete(self, storage_id: str) -> None: ...


class IAudioRepository(ABC):
    @abstractmethod
    def get_by_storage(self, storage_id: str) -> tuple[IAudioRecord, ...]: ...

    @abstractmethod
    def get_by_id(self, record_id: str) -> IAudioRecord: ...

    @abstractmethod
    def add(self, record: IAudioRecord) -> None: ...

    @abstractmethod
    def update(self, record: IAudioRecord) -> None: ...

    @abstractmethod
    def delete(self, record_id: str) -> None: ...
