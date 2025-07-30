from datetime import datetime
from uuid import uuid4

from ..interfaces import IAudioRecord


class AudioRecord(IAudioRecord):
    def __init__(
        self,
        file_name: str,
        file_path: str,
        storage_id: str,
        text: str,
        language: str,
    ):
        """
        Create AudioRecord instance with basic metadata and do transcription into text with given transcribe services.

        :param file_name: Name of audio file.
        :param file_path: Full path to audio file in some storage directory (not user storage).
        :param storage_id: Storage id of audio file.
        :param text: Text of audio file.
        :param language: Language of audio file.
        """

        self._id = uuid4().hex
        self._record_name = file_name
        self._file_path = file_path
        self._storage_id = storage_id
        self._last_updated = datetime.now()
        self._text = text
        self._language = language
        self._tags = []

    @property
    def id(self) -> str:
        """Return ID of audio record."""

        return self._id

    @id.setter
    def id(self, value: str):
        """Set ID of audio record."""
        self._id = value

    @property
    def text(self) -> str:
        """Return text of audio record."""

        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Set text for audio record."""

        self._text = value
        self._last_updated = datetime.now()

    @property
    def language(self) -> str:
        """Return language of audio file."""

        return self._language

    @property
    def tags(self) -> list:
        """Return tags of audio record."""

        return self._tags.copy()

    def add_tag(self, tag_name: str, update: bool = True) -> None:
        """Add tag to audio record. Saved in lower case."""

        if tag_name.lower() not in self._tags:
            self._tags.append(tag_name.lower())
            if update:
                self._last_updated = datetime.now()

    def remove_tag(self, tag_name: str) -> None:
        """
        Remove tag from audio record.

        :raise ValueError: If tag does not exist.
        """

        self._tags.remove(tag_name.lower())
        self._last_updated = datetime.now()

    @property
    def record_name(self) -> str:
        """Return name for the audio record."""

        return self._record_name

    @record_name.setter
    def record_name(self, note_name: str):
        """Sets the display name for the audio record."""

        self._record_name = note_name
        self._last_updated = datetime.now()

    @property
    def file_path(self) -> str:
        """Absolute filesystem path to the audio file."""

        return self._file_path

    @property
    def storage_id(self) -> str:
        """Identifier of associated storage container."""

        return self._storage_id

    @property
    def last_updated(self) -> datetime:
        """Timestamp of last modification in UTC."""

        return self._last_updated

    @last_updated.setter
    def last_updated(self, value: datetime):
        self._last_updated = value
