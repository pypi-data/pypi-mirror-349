import os

from .formats.docx_exporter import DocxExporter
from .formats.iexporter import IExporter
from ...domain.interfaces import ITextExporter


class TextExporter(ITextExporter):
    """Exporter of text (string) to different formats."""

    def __init__(self):
        self.__exporters: dict[str, IExporter] = {"docx": DocxExporter()}

    def export_text(
        self, content: str, output_dir: str, filename: str, file_format: str
    ) -> str:
        """
        Export text (string) to format.

        :param content: Target text to export.
        :param output_dir: Target output directory.
        :param filename: Filename to save the exported text.
        :param file_format: Format to save the exported text (Now only 'docx').
        :raise ValueError: If format is not supported.
        """

        if not content:
            raise ValueError("Content cannot be empty")
        if not output_dir:
            raise ValueError("Output directory cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")
        if not os.path.exists(output_dir):
            raise ValueError(f"Output directory does not exist: {output_dir}")
        if file_format not in self.__exporters:
            raise ValueError(f"Unsupported format: {file_format}")

        exporter = self.__exporters[file_format]
        output_path = f"{output_dir}/{filename}.{exporter.file_extension}"
        exporter.export(content, output_path)

        return output_path
