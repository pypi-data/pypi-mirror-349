import hashlib
import secrets

from ...domain.interfaces import IPasswordManager


class PasswordManager(IPasswordManager):
    def hash_password(self, password: str) -> str:
        """
        Hash a password.

        :param password: Password to hash.
        :return: Hash result.
        """

        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    def create_password(self) -> str:
        """
        Create password.

        :return: Not hashed password."""

        password = secrets.token_urlsafe(12)
        return password

    def verify_password(self, hashed_password: str, other: str) -> bool:
        return hashed_password == self.hash_password(other)
