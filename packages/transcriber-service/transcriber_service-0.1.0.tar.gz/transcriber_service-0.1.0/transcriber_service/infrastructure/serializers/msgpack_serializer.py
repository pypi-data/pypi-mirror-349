import msgpack

from ...domain.interfaces import ISerializer


class MsgpackSerializer(ISerializer):
    def serialize(self, data) -> bytes:
        return msgpack.packb(data, use_bin_type=True)

    def deserialize(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes")
        if not data:
            raise ValueError("Data cannot be empty")

        return msgpack.unpackb(data, raw=False)

    @property
    def extension(self) -> str:
        return "msgpack"

    @property
    def binary(self) -> bool:
        return True
