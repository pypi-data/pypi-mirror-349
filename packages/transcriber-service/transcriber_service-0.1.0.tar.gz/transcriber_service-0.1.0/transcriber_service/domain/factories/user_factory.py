from abc import ABC, abstractmethod

from ..entities.user import AuthUser, Admin
from ..interfaces import IUser


class IUserFactory(ABC):
    """Abstract base class for user factories."""

    @abstractmethod
    def create_user(self, email: str, password_hash: str) -> IUser:
        """Create a user with the given email and password hash."""
        pass


class AuthUserFactory(IUserFactory):
    """Factory for creating AuthUser instances."""

    def create_user(self, email: str, password_hash: str) -> IUser:
        return AuthUser(email, password_hash)


class AdminFactory(IUserFactory):
    """Factory for creating Admin instances."""

    def create_user(self, email: str, password_hash: str) -> IUser:
        return Admin(email, password_hash)
