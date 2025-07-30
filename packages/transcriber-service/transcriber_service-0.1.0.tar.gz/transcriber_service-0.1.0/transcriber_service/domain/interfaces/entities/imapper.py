from abc import ABC, abstractmethod


class IMapper(ABC):
    @abstractmethod
    def to_dto(self, data):
        """
        Convert the entity to a DTO.

        :return: DTO representation of the entity.
        """
        pass

    @abstractmethod
    def from_dto(self, dto):
        """
        Create an entity from a DTO.

        :param dto: DTO with entity data.
        :return: Entity instance.
        """
        pass
