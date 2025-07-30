from bson.binary import Binary
from pymongo import MongoClient
from pymongo.collection import Collection

from ....domain.interfaces import (
    IStorageRepository,
    ISerializer,
    IStorage,
)


class MongoStorageRepository(IStorageRepository):
    def __init__(
        self,
        serializer: ISerializer,
        mongo_uri: str,
        db_name: str,
        collection_name: str = "storages",
    ) -> None:

        self.__serializer = serializer

        self.__client = MongoClient(mongo_uri)
        self.__db = self.__client[db_name]
        self.__collection: Collection = self.__db[collection_name]

        self.__collection.create_index("user_id")

    def get_by_id(self, storage_id: str) -> IStorage:
        doc = self.__collection.find_one({"_id": storage_id})
        if not doc:
            raise ValueError("Storage not found")

        data = doc["data"] if self.__serializer.binary else doc["data"].decode()
        return self.__serializer.deserialize(data)

    def get_by_user(self, user_id: str) -> IStorage:
        if not user_id.strip():
            raise ValueError("user_id cannot be empty")
        doc = self.__collection.find_one({"user_id": user_id})
        if not doc:
            raise ValueError("Storage not found")

        data = doc["data"] if self.__serializer.binary else doc["data"].decode()
        return self.__serializer.deserialize(data)

    def add(self, storage: IStorage) -> None:
        if self.__collection.find_one({"_id": storage.id}):
            raise ValueError(f"Storage with ID {storage.id} already exists")
        if self.__collection.find_one({"user_id": storage.user_id}):
            raise ValueError(f"User with ID {storage.user_id} already has a storage")

        serialized = self.__serializer.serialize(storage)
        doc = {
            "_id": storage.id,
            "user_id": storage.user_id,
            "data": (
                Binary(serialized)
                if self.__serializer.binary
                else Binary(serialized.encode())
            ),
        }
        self.__collection.insert_one(doc)

    def update(self, storage: IStorage) -> None:
        if not self.__collection.find_one({"_id": storage.id}):
            raise ValueError(f"Storage with ID {storage.id} not found")

        serialized = self.__serializer.serialize(storage)
        doc = {
            "user_id": storage.user_id,
            "data": (
                Binary(serialized)
                if self.__serializer.binary
                else Binary(serialized.encode())
            ),
        }
        self.__collection.update_one({"_id": storage.id}, {"$set": doc})

    def delete(self, storage_id: str) -> None:
        doc = self.__collection.find_one({"_id": storage_id})
        if not doc:
            raise ValueError(f"Storage with ID {storage_id} not found")

        self.__collection.delete_one({"_id": storage_id})
