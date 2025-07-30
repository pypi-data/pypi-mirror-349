from datetime import datetime
from uuid import uuid4

from ..exceptions import AuthException
from ..interfaces import IUser


class User(IUser):
    """
    Represents a base user in the system.

    Handles core user properties validation and initialization.
    Should not be instantiated directly - use AuthUser or Admin subclasses.
    """

    def __init__(self, email: str, password_hash: str):
        """
        Create User instance with validated credentials.

        :param email: User's email address.
        :param password_hash: Plain-text password to be hashed.
        :raises: If email is not valid.
        """

        self._email: str = email
        self._id: str = uuid4().hex
        self._password_hash: str = password_hash
        self._temp_password_hash: str | None = None
        self._registration_date: datetime = datetime.now()
        self._last_updated: datetime = self._registration_date
        self._is_blocked: bool = False

    @property
    def is_blocked(self) -> bool:
        """Returns True if the user is blocked else False."""

        return self._is_blocked

    @is_blocked.setter
    def is_blocked(self, is_blocked: bool):
        """Sets the blocked state of the user."""

        self._is_blocked = is_blocked
        self._last_updated = datetime.now()

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password_hash: str):
        if not password_hash:
            raise AuthException("Password hash cannot be empty.")
        self._password_hash = password_hash
        self._last_updated = datetime.now()

    @property
    def temp_password_hash(self) -> str | None:
        return self._temp_password_hash

    @temp_password_hash.setter
    def temp_password_hash(self, temp_password_hash: str):
        self._temp_password_hash = temp_password_hash
        self._last_updated = datetime.now()

    @property
    def id(self) -> str:
        """Returns user ID."""

        return self._id

    @id.setter
    def id(self, id_: str):
        """Sets the user ID."""
        self._id = id_

    @property
    def email(self) -> str:
        """Returns user email."""

        return self._email

    @property
    def registration_date(self) -> datetime:
        """Returns user registration date."""

        return self._registration_date

    @property
    def last_updated(self) -> datetime:
        """Returns user last updated date."""

        return self._last_updated

    @last_updated.setter
    def last_updated(self, value: datetime):
        """Sets the user last updated date."""
        self._last_updated = value

    def can_block(self) -> bool:
        raise NotImplementedError()

    @registration_date.setter
    def registration_date(self, value: datetime):
        """Sets the user registration date."""
        self._registration_date = value


class AuthUser(User):
    """
    Represents an authenticated user with basic privileges.

    Inherits from User class and sets default role to 'user'.
    Should be used for all registered non-admin users.
    """

    def __init__(self, email: str, password_hash: str):
        super().__init__(email, password_hash)

    def can_block(self) -> bool:
        return False


class Admin(AuthUser):
    """
    Represents an administrator user with elevated privileges.

    Inherits from AuthUser and sets default role to 'admin'.
    Should be instantiated only through proper admin creation process.
    """

    def __init__(self, email: str, password_hash: str):
        super().__init__(email, password_hash)

    def can_block(self) -> bool:
        return True
