from abc import ABC, abstractmethod


class ITranscriber(ABC):
    @abstractmethod
    def transcribe(
        self,
        content: bytes,
        language: str | None,
        max_speakers: int | None,
        main_theme: str | None,
    ) -> tuple[str, str]:
        """Transcribe audio content to text and return text and detected language."""
        pass
