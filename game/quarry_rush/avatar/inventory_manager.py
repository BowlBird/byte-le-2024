import random

from game.common.enums import Company, ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.quarry_rush.entity.ores import Lambdium, Turite

from typing import Self


class InventoryManager(GameObject):
    """
    This class is used to manage Avatar inventories instead of the avatar instances doing so. This will only be
    created once in the project's lifespan, but is not enforced to be a singleton object.
    """

    __inventory_size: int = 50

    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.INVENTORY_MANAGER
        self.__inventories: dict[Company, list[Item | None]]

    def get_inventory(self, company: Company) -> list[Item | None]:
        return self.__inventories[company]

    def is_empty(self, company: Company) -> bool:
        """
        Returns True if first index is None, returns False otherwise
        """
        if self.__inventories[company][0] is None:
            return True
        else:
            return False

