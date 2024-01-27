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
        self.__inventories: dict[Company, list[Item | None]] = {
            Company.CHURCH: self.create_empty_inventory(),
            Company.TURING: self.create_empty_inventory()
        }

    def create_empty_inventory(self) -> list[Item | None]:
        ...

    def cash_in_science(self, company: Company) -> int:
        ...

    def cash_in_points(self, company: Company) -> int:
        ...

    def cash_in_all(self, company: Company) -> tuple[int, int]:
        ...

    def give(self, item: Item | None, company: Company, drop_rate: int = 1) -> bool:
        ...

    def take(self, item: Item, company: Company) -> bool:
        ...

    def steal(self, to_company: Company, from_company: Company, steal_rate: float) -> None:
        ...

    def is_empty(self, company: Company) -> bool:
        ...

    def maybe_item_json(self, item: Item | None) -> dict | None:
        ...
    
    def inventories_json(self) -> dict:
        ...
            
    def maybe_item_from_json(self, item: dict | None) -> Item | None:
        ...
            
    def from_inventories_json(self, data: dict) -> dict:
        ...

    def to_json(self):
        ...

    def from_json(self, data: dict) -> Self:
        ...
