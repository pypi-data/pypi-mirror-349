from datetime import datetime

from .dto.audio_record_dto import AudioRecordDTO
from ...domain.factories import AudioRecordFactory, IAudioRecordFactory
from ...domain.interfaces import IMapper, IAudioRecord


class AudioRecordMapper(IMapper):
    def __init__(self, factory: IAudioRecordFactory = AudioRecordFactory()):
        self._factory = factory

    def to_dto(self, audio: IAudioRecord) -> AudioRecordDTO:
        if not isinstance(audio, IAudioRecord):
            raise TypeError("Object must be an IAudioRecord instance")

        return AudioRecordDTO(
            entity_type="audiorecord",
            id=audio.id,
            record_name=audio.record_name,
            file_path=audio.file_path,
            storage_id=audio.storage_id,
            text=audio.text,
            language=audio.language,
            tags=audio.tags,
            last_updated=audio.last_updated.isoformat(),
        )

    def from_dto(self, dto: AudioRecordDTO) -> IAudioRecord:
        audio = self._factory.create_audio(
            file_name=dto.record_name,
            file_path=dto.file_path,
            storage_id=dto.storage_id,
            text=dto.text or "",
            language=dto.language or "",
        )
        audio.id = dto.id
        audio.last_updated = datetime.fromisoformat(dto.last_updated)
        for tag in dto.tags:
            audio.add_tag(tag, False)

        return audio
