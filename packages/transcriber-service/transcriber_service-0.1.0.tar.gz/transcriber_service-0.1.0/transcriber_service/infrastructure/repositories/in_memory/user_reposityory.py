from ....domain.interfaces import (
    IUser,
    IUserRepository,
    ISerializer,
    IFileManager,
)


class LocalUserRepository(IUserRepository):
    def __init__(
        self, data_dir: str, file_manager: IFileManager, serializer: ISerializer
    ):
        """
        Create local user repository.

        :param data_dir: Directory to store local user data.
        """

        self.__serializer = serializer
        self.__file_manager = file_manager
        self._users: dict[str, IUser] = {}
        self.__dir: str = data_dir

        try:
            self._users = self.__file_manager.load(data_dir, self.__serializer)
        except Exception as e:
            pass

    def get_by_id(self, user_id: str) -> IUser | None:
        """Return user by its ID if it exists else None."""

        return self._users.get(user_id)

    def get_by_email(self, email: str) -> IUser | None:
        """Return user by email if it exists else None."""

        return next((u for u in self._users.values() if u.email == email), None)

    def add(self, user: IUser) -> None:
        """
        Add user to repository.

        :param user: New user.
        :raise ValueError: If user already exists.
        """

        if user.id in self._users:
            raise ValueError("User already exists")
        self._users[user.id] = user
        self.__save()

    def update(self, user: IUser) -> None:
        """
        Update user in repository.

        :param user: New user value.
        :raise ValueError: If user does not exist.
        """

        if user.id not in self._users:
            raise ValueError("User not found")
        self._users[user.id] = user
        self.__save()

    def delete(self, user: IUser) -> None:
        """
        Delete user from repository.

        :param user: Target user.
        :raise ValueError: If user does not exist.
        """

        if user.id not in self._users:
            raise ValueError("User not found")
        self._users.pop(user.id)
        self.__save()

    def get_all(self) -> list[IUser]:
        """Return all users in repository."""

        return list(self._users.values())

    def __save(self):
        self.__file_manager.save(self._users, self.__dir, self.__serializer)
