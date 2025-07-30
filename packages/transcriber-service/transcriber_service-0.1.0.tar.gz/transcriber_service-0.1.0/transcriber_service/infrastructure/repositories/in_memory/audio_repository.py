from ....domain.interfaces import (
    IAudioRepository,
    IStorageRepository,
    IAudioRecord,
    IFileManager,
    ISerializer,
)


class LocalAudioRepository(IAudioRepository):
    def __init__(
        self,
        storage_repository: IStorageRepository,
        data_dir: str,
        file_manager: IFileManager,
        serializer: ISerializer,
    ) -> None:
        """
        Create local audio repository.

        :type storage_repository: IStorageRepository.
        :param data_dir: Directory to store local audio data.
        """
        self.__serializer = serializer
        self.__file_manager = file_manager
        self.__records: dict[str, IAudioRecord] = {}
        self.__storage_repository = storage_repository
        self.__dir = data_dir

        try:
            self.__records = file_manager.load(self.__dir, serializer)
        except:
            self.__records = {}

    def get_by_storage(self, storage_id: str) -> tuple[IAudioRecord, ...]:
        """Return list of audio records by storage id."""
        return tuple(r for r in self.__records.values() if r.storage_id == storage_id)

    def get_by_id(self, record_id: str) -> IAudioRecord | None:
        """Return audio record by id if it exists else None."""

        return self.__records.get(record_id)

    def add(self, record: IAudioRecord) -> None:
        """
        Add audio record to repository.

        :raise ValueError: If audio record already exists.
        """

        if record.id in self.__records:
            raise ValueError("Record already exists.")

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.add_audio_record(record.id)
            self.__storage_repository.update(storage)
            self.__records[record.id] = record
            self.__save()

    def update(self, record: IAudioRecord) -> None:
        """
        Update audio record from repository with new value.

        :param record: new value of audio record.
        :raise ValueError: If audio record does not exist.
        """

        if record.id not in self.__records:
            raise ValueError("Record not found.")
        self.__records[record.id] = record
        self.__save()

    def delete(self, record_id: str) -> None:
        """
        Delete audio record from repository.

        :param record_id: ID of target audio record.
        :raise ValueError: If audio record does not exist.
        """

        record = self.__records.get(record_id)
        if not record:
            raise ValueError("Record not found.")

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.remove_audio_record(record_id)
            self.__storage_repository.update(storage)

        del self.__records[record_id]
        self.__save()

    def __save(self) -> None:
        self.__file_manager.save(self.__records, self.__dir, self.__serializer)
