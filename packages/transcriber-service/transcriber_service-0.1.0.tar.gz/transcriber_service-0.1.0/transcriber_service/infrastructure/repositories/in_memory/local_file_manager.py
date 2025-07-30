from pathlib import Path

from ....domain.interfaces import ISerializer, IFileManager


class LocalFileManager(IFileManager):
    @staticmethod
    def save(data, filename: str, serializer: ISerializer) -> None:
        """Save data to file."""
        if not filename:
            raise ValueError("filename cannot be empty")

        filename = f"{filename}.{serializer.extension}"
        data = serializer.serialize(data)
        binary = serializer.binary

        file_path = Path(filename)

        with open(file_path, "wb" if binary else "w") as f:
            f.write(data)

    @staticmethod
    def load(filename: str, serializer: ISerializer):
        """Load data from file."""
        if not filename:
            raise ValueError("filename cannot be empty")

        filename = f"{filename}.{serializer.extension}"
        binary = serializer.binary

        with open(filename, "rb" if binary else "r") as f:
            data = f.read()

            return serializer.deserialize(data) if serializer else data
