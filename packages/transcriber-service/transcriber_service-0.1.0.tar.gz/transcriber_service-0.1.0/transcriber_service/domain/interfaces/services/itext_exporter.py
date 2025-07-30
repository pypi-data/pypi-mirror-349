from abc import ABC, abstractmethod


class ITextExporter(ABC):
    @abstractmethod
    def export_text(
        self, content: str, output_dir: str, filename: str, file_format: str
    ) -> str:
        """
        Export text (string) to format.

        :param content: Target text to export.
        :param output_dir: Target output directory.
        :param filename: Filename to save the exported text.
        :param file_format: Format to save the exported text.
        """
        pass
