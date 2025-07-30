from bson.binary import Binary
from pymongo import MongoClient
from pymongo.collection import Collection

from ....domain.interfaces import IUserRepository, ISerializer, IUser


class MongoUserRepository(IUserRepository):
    def __init__(
        self,
        serializer: ISerializer,
        mongo_uri: str,
        db_name: str,
        collection_name: str = "users",
    ) -> None:

        self.__serializer = serializer

        self.__client = MongoClient(mongo_uri)
        self.__db = self.__client[db_name]

        self.__collection: Collection = self.__db[collection_name]
        self.__collection.create_index("email", unique=True)

    def get_by_id(self, user_id: str) -> IUser | None:
        doc = self.__collection.find_one({"_id": user_id})
        if doc is None:
            return None

        data = doc["data"] if self.__serializer.binary else doc["data"].decode()
        return self.__serializer.deserialize(data)

    def get_by_email(self, user_id: str) -> IUser | None:
        doc = self.__collection.find_one({"email": user_id})
        if doc is None:
            return None

        data = doc["data"] if self.__serializer.binary else doc["data"].decode()
        return self.__serializer.deserialize(data)

    def add(self, user: IUser) -> None:
        if self.__collection.find_one({"_id": user.id}):
            raise ValueError(f"User with ID {user.id} already exists")
        if self.__collection.find_one({"email": user.email}):
            raise ValueError(f"User with email {user.email} already exists")

        serialized = self.__serializer.serialize(user)
        doc = {
            "_id": user.id,
            "email": user.email,
            "data": (
                Binary(serialized)
                if self.__serializer.binary
                else Binary(serialized.encode())
            ),
        }

        self.__collection.insert_one(doc)

    def update(self, user: IUser) -> None:
        if not self.__collection.find_one({"_id": user.id}):
            raise ValueError(f"User with ID {user.id} not found")

        serialized = self.__serializer.serialize(user)
        doc = {
            "email": user.email,
            "data": (
                Binary(serialized)
                if self.__serializer.binary
                else Binary(serialized.encode())
            ),
        }

        self.__collection.update_one({"_id": user.id}, {"$set": doc})

    def delete(self, user: IUser) -> None:
        if not self.__collection.find_one({"_id": user.id}):
            raise ValueError(f"User with ID {user.id} not found")

        self.__collection.delete_one({"_id": user.id})

    def get_all(self) -> list[IUser]:
        users = self.__collection.find()
        users = [self.get_by_id(user["_id"]) for user in users]

        return users
