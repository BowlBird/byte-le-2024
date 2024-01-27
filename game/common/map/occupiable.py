from __future__ import annotations

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from typing import Self, Type


class Occupiable(GameObject):
    """
    `Occupiable Class Notes:`

        Occupiable objects exist to encapsulate all objects that could be placed on the gameboard.

        These objects can only be occupied by GameObjects, so inheritance is important. The ``None`` value is
        acceptable for this too, showing that nothing is occupying the object.

        Note: The class Item inherits from GameObject, but it is not allowed to be on an Occupiable object.
    """

    def __init__(self, occupied_by: GameObject = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.OCCUPIABLE
        self.occupied_by: GameObject | None = occupied_by

    @property
    def occupied_by(self) -> GameObject | None:
        return self.__occupied_by

    @occupied_by.setter
    def occupied_by(self, occupied_by: GameObject | None) -> None:
        if occupied_by is not None and isinstance(occupied_by, Item):
            raise ValueError(f'{self.__class__.__name__}.occupied_by cannot be an Item.')
        if occupied_by is not None and not isinstance(occupied_by, GameObject):
            raise ValueError(f'{self.__class__.__name__}.occupied_by must be None or an instance of GameObject.')
        self.__occupied_by = occupied_by

    def place_on_top_of_stack(self, game_object: GameObject) -> bool:
        ...

    def is_occupied_by_object_type(self, object_type: ObjectType) -> bool:
        ...

    def is_occupied_by_game_object(self, game_object_type: Type) -> bool:
        ...

    def get_occupied_by(self, target: ObjectType | GameObject) -> GameObject | None:
        ...

    def remove_from_occupied_by(self, object_type: ObjectType | None = None) -> GameObject | None:
        ...

    def remove_game_object_from_occupied_by(self, game_object: GameObject | None = None) -> GameObject | None:
        ...
