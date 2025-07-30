import json

from ...domain.interfaces.services.iserializer import ISerializer


class JsonSerializer(ISerializer):
    def serialize(self, data) -> str:
        return json.dumps(data)

    def deserialize(self, data: str):
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        if not data.strip():
            raise ValueError("Data cannot be empty")

        data_dict = json.loads(data)
        return data_dict

    @property
    def extension(self) -> str:
        return "json"

    @property
    def binary(self) -> bool:
        return False
