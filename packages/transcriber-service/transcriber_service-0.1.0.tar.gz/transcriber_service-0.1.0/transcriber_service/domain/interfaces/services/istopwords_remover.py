from abc import ABC, abstractmethod


class IStopwordsRemover(ABC):
    @abstractmethod
    def remove_stopwords(
        self, text: str, remove_swear_words: bool, go_few_times: bool
    ) -> str:
        """Remove stopwords from text."""
        pass

    @abstractmethod
    def remove_words(self, text: str, words: list[str] | tuple[str]) -> str:
        """Remove specific words from text."""
        pass
