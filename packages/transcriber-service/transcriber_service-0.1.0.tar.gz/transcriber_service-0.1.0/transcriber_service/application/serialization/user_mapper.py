from datetime import datetime

from .dto.user_dto import UserDTO
from ...domain.entities.user import Admin
from ...domain.factories import AuthUserFactory, AdminFactory, IUserFactory
from ...domain.interfaces import IMapper, IUser


class UserMapper(IMapper):
    def __init__(self):
        self._factories: dict[str, IUserFactory] = {
            "authuser": AuthUserFactory(),
            "admin": AdminFactory(),
        }

    def to_dto(self, user: IUser) -> UserDTO:
        if not isinstance(user, IUser):
            raise TypeError("Object must be a IUser instance")

        entity_type = "admin" if isinstance(user, Admin) else "authuser"

        return UserDTO(
            entity_type=entity_type,
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            registration_date=user.registration_date.isoformat(),
            last_updated=user.last_updated.isoformat(),
            is_blocked=user.is_blocked,
            temp_password_hash=user.temp_password_hash,
        )

    def from_dto(self, dto: UserDTO) -> IUser:
        factory = self._factories.get(dto.entity_type)
        if not factory:
            raise ValueError(f"Invalid entity_type: {dto.entity_type}")

        user = factory.create_user(dto.email, dto.password_hash)

        if dto.temp_password_hash:
            user.temp_password_hash = dto.temp_password_hash

        user.is_blocked = dto.is_blocked
        user.id = dto.id
        user.last_updated = datetime.fromisoformat(dto.last_updated)
        user.registration_date = datetime.fromisoformat(dto.registration_date)

        return user
