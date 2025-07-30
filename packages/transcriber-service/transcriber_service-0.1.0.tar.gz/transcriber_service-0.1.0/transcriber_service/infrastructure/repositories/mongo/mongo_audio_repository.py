from bson.binary import Binary
from pymongo import MongoClient
from pymongo.collection import Collection

from ....domain.interfaces import (
    IAudioRepository,
    IStorageRepository,
    ISerializer,
    IAudioRecord,
)


class MongoAudioRepository(IAudioRepository):
    def __init__(
        self,
        storage_repository: IStorageRepository,
        serializer: ISerializer,
        mongo_uri: str,
        db_name: str,
        collection_name: str = "audio_records",
    ) -> None:

        self.__serializer = serializer
        self.__storage_repository = storage_repository

        self.__client = MongoClient(mongo_uri)
        self.__db = self.__client[db_name]

        self.__collection: Collection = self.__db[collection_name]
        self.__collection.create_index("storage_id")
        self.__collection.create_index("tags")

    def get_by_storage(self, storage_id: str) -> tuple[IAudioRecord, ...]:
        if not storage_id.strip():
            raise ValueError("Storage ID cannot be empty")

        documents = self.__collection.find({"storage_id": storage_id})
        return tuple(
            self.__serializer.deserialize(
                doc["data"] if self.__serializer.binary else doc["data"].decode()
            )
            for doc in documents
            if "data" in doc
        )

    def get_by_id(self, record_id: str) -> IAudioRecord:
        if not record_id.strip():
            raise ValueError("Record ID cannot be empty")
        doc = self.__collection.find_one({"_id": record_id})
        if not doc:
            raise ValueError("Record ID not found")

        data = doc["data"] if self.__serializer.binary else doc["data"].decode()
        return self.__serializer.deserialize(data)

    def add(self, record: IAudioRecord) -> None:
        if self.__collection.find_one({"_id": record.id}):
            raise ValueError(f"Record with ID {record.id} already exists")

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {record.storage_id} not found")

        storage.add_audio_record(record.id)
        self.__storage_repository.update(storage)

        serialized = self.__serializer.serialize(record)
        doc = {
            "_id": record.id,
            "storage_id": record.storage_id,
            "tags": record.tags,
            "data": (
                Binary(serialized)
                if self.__serializer.binary
                else Binary(serialized.encode())
            ),
        }
        self.__collection.insert_one(doc)

    def update(self, record: IAudioRecord) -> None:
        if not self.__collection.find_one({"_id": record.id}):
            raise ValueError(f"Record with ID {record.id} not found")

        serialized = self.__serializer.serialize(record)
        doc = {
            "storage_id": record.storage_id,
            "tags": record.tags,
            "data": (
                Binary(serialized)
                if self.__serializer.binary
                else Binary(serialized.encode())
            ),
        }
        self.__collection.update_one({"_id": record.id}, {"$set": doc})

    def delete(self, record_id: str) -> None:
        doc = self.__collection.find_one({"_id": record_id})
        if not doc:
            raise ValueError(f"Record with ID {record_id} not found")

        record = self.__serializer.deserialize(
            doc["data"] if self.__serializer.binary else doc["data"].decode()
        )
        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.remove_audio_record(record_id)
            self.__storage_repository.update(storage)

        self.__collection.delete_one({"_id": record_id})
