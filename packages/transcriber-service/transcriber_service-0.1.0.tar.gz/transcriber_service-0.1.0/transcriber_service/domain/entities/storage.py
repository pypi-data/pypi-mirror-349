from uuid import uuid4

from ..interfaces import IStorage


class Storage(IStorage):
    def __init__(self, user_id: str):
        """
        Represents a user's personal storage container for audio records.

        :param user_id: The user's ID (only one user for storage).
        """

        self._id = uuid4().hex
        self._user_id = user_id
        self._audio_record_ids: list[str] = []

    @property
    def id(self) -> str:
        """Return ID of the storage container."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def user_id(self) -> str:
        """Return the ID of owner user."""
        return self._user_id

    @property
    def audio_record_ids(self) -> list[str]:
        """Return a list of audio record IDs."""
        return self._audio_record_ids.copy()

    def add_audio_record(self, record_id: str) -> None:
        """
        Add audio record to storage.

        :param record_id: The audio record ID to add.
        :return: None
        """
        if record_id not in self._audio_record_ids:
            self._audio_record_ids.append(record_id)

    def remove_audio_record(self, record_id: str) -> None:
        """
        Remove audio record from storage.

        :param record_id: The audio record ID to remove.
        :return: None
        :raise ValueError: If record_id is not in the list of audio record IDs.
        """
        self._audio_record_ids.remove(record_id)
