import logging

from email_validator import validate_email
from password_strength import PasswordPolicy

from .user_service import UserService
from ..serialization.dto import UserDTO
from ..serialization.user_mapper import UserMapper
from ...domain import AuthException
from ...domain.factories import (
    AuthUserFactory,
    IUserFactory,
    AdminFactory,
)
from ...domain.interfaces import IEmailService, IPasswordManager

logger = logging.getLogger(__name__)


class AuthService(object):
    """
    Represents an authentication services.
    Supports login, register, changing and recovering password, blocking and unblocking of users.
    """

    def __init__(
        self,
        user_service: UserService,
        email_service: IEmailService,
        password_hasher: IPasswordManager,
    ):
        self._user_service = user_service
        self._password_manager = password_hasher
        self._policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )
        self.mapper = UserMapper()
        self.__email_service = email_service

    def _register(self, email: str, password: str, factory: IUserFactory) -> UserDTO:
        if self._user_service.get_user_by_email(email):
            logger.error(f"User with email {email} already exists")
            raise ValueError("User already exists")

        errors = self._policy.test(password)
        if errors:
            logger.error(f"Error validating password: {errors}, {password}")
            raise AuthException(
                f"Password is weak: 8 symbols, 1 uppercase, number, special"
            )

        email = validate_email(email).normalized
        password_hash = self._password_manager.hash_password(password)
        user = self._user_service.create_user(email, password_hash, factory)

        return self.mapper.to_dto(user)

    def register_user(self, email: str, password: str) -> UserDTO:

        return self._register(email, password, AuthUserFactory())

    def create_admin(self, email: str, password: str) -> UserDTO:
        return self._register(email, password, AdminFactory())

    def login(self, email: str, password: str) -> UserDTO:

        user = self._user_service.get_user_by_email(email)
        if not user or not password:
            logger.warning(f"User {email} not found or no password.")
            raise AuthException("Invalid credentials")
        if user.temp_password_hash and self._password_manager.verify_password(
            user.temp_password_hash, password
        ):
            logger.info(f"User {email} use temp password.")
            user.password_hash = user.temp_password_hash
            user.temp_password_hash = None
            self._user_service.update_user(user)
        if not self._password_manager.verify_password(user.password_hash, password):
            logger.warning(f"User {email} login unsuccessful.")
            raise AuthException("Invalid credentials")

        if user.is_blocked:
            raise AuthException("User is blocked")

        return self.mapper.to_dto(user)

    def change_password(
        self, email: str, current_password: str, new_password: str
    ) -> None:

        user = self._user_service.get_user_by_email(email)
        if not user:
            raise AuthException("User not found")

        errors = self._policy.test(new_password)
        if errors:
            raise AuthException(f"Password is weak: {errors}")
        if not self._password_manager.verify_password(
            user.password_hash, current_password
        ):
            raise AuthException("Incorrect password")

        user.password_hash = self._password_manager.hash_password(new_password)
        self._user_service.update_user(user)

    def recover_password(self, email: str) -> None:
        user = self._user_service.get_user_by_email(email)
        if not user:
            raise AuthException("User not found")

        temp_password = self._password_manager.create_password()
        temp_password_hash = self._password_manager.hash_password(temp_password)
        user.temp_password_hash = temp_password_hash

        self.__email_service.send_recovery_email(user.email, temp_password)
        self._user_service.update_user(user)
