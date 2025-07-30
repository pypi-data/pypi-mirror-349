from abc import ABC, abstractmethod
from datetime import datetime


class IUser(ABC):
    @property
    @abstractmethod
    def is_blocked(self) -> bool:
        """Returns True if the user is blocked else False."""
        pass

    @is_blocked.setter
    @abstractmethod
    def is_blocked(self, is_blocked: bool):
        """Sets the blocked state of the user."""
        pass

    @property
    @abstractmethod
    def password_hash(self) -> str:
        pass

    @password_hash.setter
    @abstractmethod
    def password_hash(self, password_hash: str):
        pass

    @property
    @abstractmethod
    def temp_password_hash(self) -> str | None:
        pass

    @temp_password_hash.setter
    @abstractmethod
    def temp_password_hash(self, temp_password_hash: str):
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        """Returns user ID."""
        pass

    @id.setter
    @abstractmethod
    def id(self, id_: str): ...

    @property
    @abstractmethod
    def email(self) -> str:
        """Returns user email."""
        pass

    @property
    @abstractmethod
    def registration_date(self) -> datetime:
        """Returns user registration date."""
        pass

    @property
    @abstractmethod
    def last_updated(self) -> datetime:
        """Returns user last updated date."""
        pass

    @last_updated.setter
    @abstractmethod
    def last_updated(self, last_updated: datetime): ...

    @abstractmethod
    def can_block(self) -> bool:
        pass

    @registration_date.setter
    @abstractmethod
    def registration_date(self, value):
        pass
