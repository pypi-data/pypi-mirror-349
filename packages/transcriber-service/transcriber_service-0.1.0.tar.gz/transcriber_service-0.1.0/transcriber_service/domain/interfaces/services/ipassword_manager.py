from abc import ABC, abstractmethod


class IPasswordManager(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Hash a password.

        :param password: Password to hash.
        :return: Hash result.
        """
        pass

    @abstractmethod
    def create_password(self) -> str:
        """
        Create password.

        :return: Not hashed password."""

        pass

    @abstractmethod
    def verify_password(self, hashed_password: str, other: str) -> bool:
        pass
