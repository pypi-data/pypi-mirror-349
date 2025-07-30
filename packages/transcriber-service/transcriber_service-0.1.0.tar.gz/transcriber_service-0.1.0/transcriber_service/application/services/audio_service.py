import logging

from ..serialization.audio_mapper import (
    AudioRecordDTO,
    AudioRecordMapper,
)
from ...domain.factories import IAudioRecordFactory, AudioRecordFactory
from ...domain.interfaces import (
    IAudioRepository,
    ITextExporter,
    IStopwordsRemover,
    ITranscriber,
)
from ...domain.services.audio_search_service import AudioSearchService

logger = logging.getLogger(__name__)


class AudioRecordService(object):
    """
    Service class for managing audio records and their lifecycle operations.

    Provides functionality to create and retrieve audio records with optional
    transcription processing.
    """

    def __init__(
        self,
        repo: IAudioRepository,
        transcriber: ITranscriber,
    ):
        self._MAX_SIZE = 1024 * 1024 * 10
        self._repository = repo
        self._transcriber = transcriber
        self._audio_factory: IAudioRecordFactory = AudioRecordFactory()
        self._search_service = AudioSearchService()
        self.mapper = AudioRecordMapper()

    def create_audio(
        self,
        file_name: str,
        content: bytes,
        file_path: str,
        storage_id: str,
        language: str = None,
        max_speakers: int = None,
        main_theme: str = None,
    ) -> AudioRecordDTO:
        """
        Create AudioRecord instance with basic metadata and do transcription
        into text with given transcribe services.

        :param file_name: Name of audio file.
        :param content: Content of audio file (mp3).
        :param file_path: Full path to audio file in some storage directory
        (not user storage).
        :param storage_id: Storage id of audio file.
        :param language: Language of audio file (defaults None).
        :param max_speakers: Max number of speakers (defaults None).
        :param main_theme: Main theme of audio file (defaults None).
        :return: Created Audio Record.
        """

        if len(content) > self._MAX_SIZE:
            raise Exception("Audio file too large.")
        text, language = self._transcriber.transcribe(
            content, language, max_speakers, main_theme
        )
        audio = self._audio_factory.create_audio(
            file_name, file_path, storage_id, text, language
        )
        self._repository.add(audio)
        return self.mapper.to_dto(audio)

    def get_records(self, storage_id: str) -> tuple[AudioRecordDTO, ...]:
        """
        Retrieves audio record by its storage container ID.

        :param storage_id: Storage id of audio file.
        :return: Tuple of audio records if it is found else None.
        """
        records = self._repository.get_by_storage(storage_id)
        return tuple(self.mapper.to_dto(record) for record in records)

    def get_by_id(self, record_id: str) -> AudioRecordDTO:
        record = self._repository.get_by_id(record_id)
        return self.mapper.to_dto(record)

    def search_by_tags(
        self, storage_id: str, tags: list[str], match_all: bool = False
    ) -> list[AudioRecordDTO]:

        records = self._repository.get_by_storage(storage_id)
        matching_records = self._search_service.search_by_tags(records, tags, match_all)
        return [self.mapper.to_dto(record) for record in matching_records]

    def search_by_name(self, storage_id: str, name: str) -> list[AudioRecordDTO]:

        records = self._repository.get_by_storage(storage_id)
        matching_records = self._search_service.search_by_name(records, name)
        return [self.mapper.to_dto(record) for record in matching_records]

    def delete(self, record_id):
        self._repository.delete(record_id)


class AudioTagService(object):
    def __init__(self, repository: IAudioRepository):
        self._repository = repository

    def add_tag_to_record(self, record_id: str, tag: str) -> None:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError("Record not found")

        record.add_tag(tag)
        self._repository.update(record)

    def remove_tag_from_record(self, record_id: str, tag: str) -> None:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError("Record not found")

        try:
            record.remove_tag(tag)
            self._repository.update(record)
        except ValueError:
            pass


class AudioTextService(object):
    def __init__(
        self,
        repository: IAudioRepository,
        export_service: ITextExporter,
        stopwords_remover: IStopwordsRemover,
    ):
        self._repository = repository
        self._export_service = export_service
        self._stopwords_remover = stopwords_remover

    def export_record_text(
        self, record_id: str, output_dir: str, file_format: str
    ) -> str:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError("Audio record not found")

        return self._export_service.export_text(
            record.text, output_dir, record.record_name, file_format
        )

    def remove_stopwords(
        self,
        record_id: str,
        remove_swear_words: bool = True,
        go_few_times: bool = False,
    ) -> None:
        record = self._repository.get_by_id(record_id)
        if not record:
            logger.warning("Audio record not found")
            raise ValueError("Audio record not found")
        if record.language.lower() not in ["ru", "russian"]:
            logger.warning(f"Unsupported language: {record.language}")
            raise ValueError(f"Unsupported language: {record.language}")
        logger.info(f"Removing stopwords for text: {record.text}")

        updated_text = self._stopwords_remover.remove_stopwords(
            record.text, remove_swear_words, go_few_times
        )

        logger.info(f"Text after removing stopwords: {updated_text}")
        record.text = updated_text
        self._repository.update(record)

    def remove_words(self, record_id: str, words: list | tuple) -> None:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError("Audio record not found")
        if record.language.lower() not in ("ru", "russian"):
            raise ValueError(f"Unsupported language: {record.language}")

        record.text = self._stopwords_remover.remove_words(record.text, words)
        self._repository.update(record)

    def change_record_name(self, record_id: str, name: str) -> None:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError("Record not found")

        record.record_name = name
        self._repository.update(record)
