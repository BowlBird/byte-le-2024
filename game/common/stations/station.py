from typing import Self

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.entity.ores import *


# create Station object from GameObject that allows item to be contained in it
class Station(GameObject):
    """
    A Station is an Object that inherits from GameObject. Stations are able to contain Items in them. Players can
    interact with Stations to receive the items. (Refer to avatar.py and item.py to see how this works).
    """

    def __init__(self, held_item: Item | None = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.STATION
        self.held_item: Item | None = held_item

    # held_item getter and setter methods
    @property
    def held_item(self) -> Item | None:
        return self.__item

    @held_item.setter
    def held_item(self, held_item: Item) -> None:
        if held_item is not None and not isinstance(held_item, Item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be an Item or None, not {held_item}.')
        self.__item = held_item

    # InventoryManager added to this method for Byte-le 2024
    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager) -> Item | None:
        ...
