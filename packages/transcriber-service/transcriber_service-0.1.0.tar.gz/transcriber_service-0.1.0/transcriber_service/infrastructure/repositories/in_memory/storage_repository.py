from copy import copy

from ....domain.interfaces import (
    IStorageRepository,
    IStorage,
    ISerializer,
    IFileManager,
)


class LocalStorageRepository(IStorageRepository):
    def __init__(
        self, data_dir: str, file_manager: IFileManager, serializer: ISerializer
    ):
        """
        Create local storage repository.

        :param data_dir: Directory to store local storage data.
        """

        self.__serializer: ISerializer = serializer
        self.__storages: dict[str, IStorage] = {}
        self.__file_manager: IFileManager = file_manager
        self.__user_storage_map: dict[str, str] = {}
        self.__dir: str = data_dir

        try:
            self.__storages, self.__user_storage_map = self.__file_manager.load(
                data_dir,
                self.__serializer,
            )
        except:
            pass

    def get_by_id(self, storage_id: str) -> IStorage | None:
        """Return storage object copy if it exists by ID else None."""

        return copy(self.__storages.get(storage_id))

    def get_by_user(self, user_id: str) -> IStorage | None:
        """Return storage object copy if it exists by user_id else None."""

        storage_id = self.__user_storage_map.get(user_id)
        return self.__storages.get(storage_id) if storage_id else None

    def add(self, storage: IStorage) -> None:
        """
        Add storage object to storage repository.

        :param storage: Storage object.
        :raise ValueError: If storage already exists.
        """

        if storage.id in self.__storages:
            raise ValueError("Storage already exists")

        self.__storages[storage.id] = storage
        self.__user_storage_map[storage.user_id] = storage.id
        self.__save()

    def update(self, storage: IStorage) -> None:
        """
        Update storage object in storage repository.

        :param storage: New storage value.
        :raise ValueError: If storage does not exist.
        """

        if storage.id not in self.__storages:
            raise ValueError("Storage not found")
        self.__storages[storage.id] = storage
        self.__save()

    def delete(self, storage_id: str) -> None:
        if storage_id not in self.__storages:
            raise ValueError("Storage not found")

        del self.__storages[storage_id]
        self.__save()

    def __save(self):
        self.__file_manager.save(
            (self.__storages, self.__user_storage_map),
            self.__dir,
            self.__serializer,
        )
