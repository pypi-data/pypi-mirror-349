from audio_transcribing import Transcriber as BaseTranscriber

from ...domain.interfaces import ITranscriber


class Transcriber(ITranscriber):
    def __init__(
        self,
        token: str,
        whisper_model: str = "medium",
        speaker_diarization_model: str = "pyannote/speaker-diarization-3.1",
        use_faster_whisper: bool = False,
    ):
        self._transcriber = BaseTranscriber(
            token, whisper_model, speaker_diarization_model, use_faster_whisper
        )

    def transcribe(
        self,
        content: bytes,
        language: str | None,
        max_speakers: int | None,
        main_theme: str | None,
    ) -> tuple[str, str]:
        return self._transcriber.transcribe(content, language, max_speakers, main_theme)
