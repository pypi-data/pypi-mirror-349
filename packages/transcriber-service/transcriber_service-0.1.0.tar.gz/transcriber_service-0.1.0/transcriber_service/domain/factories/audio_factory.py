from abc import ABC, abstractmethod

from ..entities.audio import AudioRecord
from ..interfaces import IAudioRecord


class IAudioRecordFactory(ABC):

    @abstractmethod
    def create_audio(
        self,
        file_name: str,
        file_path: str,
        storage_id: str,
        text: str,
        language: str,
    ) -> IAudioRecord:
        pass


class AudioRecordFactory(IAudioRecordFactory):

    def create_audio(
        self,
        file_name: str,
        file_path: str,
        storage_id: str,
        text: str,
        language: str,
    ) -> IAudioRecord:
        return AudioRecord(file_name, file_path, storage_id, text, language)
