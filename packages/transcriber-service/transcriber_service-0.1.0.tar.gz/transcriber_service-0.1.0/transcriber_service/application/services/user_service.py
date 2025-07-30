import logging

from password_strength import PasswordPolicy

from .storage_service import StorageService
from ...domain.factories import (
    IUserFactory,
)
from ...domain.interfaces import (
    IUserRepository,
    IUser,
)

logger = logging.getLogger(__name__)


class UserService(object):
    def __init__(
        self,
        repository: IUserRepository,
        storage_service: StorageService,
    ):
        self._repository = repository
        self._storage_service = storage_service
        self._user_factory: IUserFactory | None = None
        self._policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )

    def create_user(self, email: str, password: str, factory: IUserFactory) -> IUser:
        self._user_factory = factory
        user = self._user_factory.create_user(email, password)

        self._repository.add(user)
        self._storage_service.create_storage(user.id)

        return user

    def delete_user(self, user: IUser):
        self._repository.delete(user)

    def get_user_by_email(self, email: str) -> IUser | None:
        return self._repository.get_by_email(email)

    def update_user(self, user: IUser):
        self._repository.update(user)

    def get_by_id(self, user_id: str) -> IUser | None:
        return self._repository.get_by_id(user_id)

    def get_all(self) -> list[IUser]:
        return self._repository.get_all()

    def set_blocked(self, initiator: IUser, target_email: str, block: bool) -> None:
        if not initiator.can_block():
            raise PermissionError("Only admins can block users")

        user = self.get_user_by_email(target_email)
        if not user:
            raise KeyError("User not found")

        user.is_blocked = block
        self.update_user(user)

    def delete(self, initiator: IUser, target_email: str):
        if not initiator.can_block():
            raise PermissionError("Only admins can delete users")

        user = self.get_user_by_email(target_email)
        if not user:
            raise KeyError("User not found")

        self.delete_user(user)
