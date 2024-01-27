from __future__ import annotations
from typing import Callable, TypeVar, Generic, Self
from game.quarry_rush.tech.tech import Tech, techs, TechInfo
from game.quarry_rush.avatar.avatar_functions import AvatarFunctions
from functools import reduce
from game.common.game_object import GameObject


class TechTree(GameObject):
    """
    Represents a single player's tech tree

    Contains all functionality for researching and tech effects

    [Note]: This class does not handle cost validation or taking research points away from the player
    """

    def __init__(self, avatar_functions: AvatarFunctions):
        super().__init__()
        ...

    def tech_names(self) -> list[str]:
        """
        Returns a list of all techs that are in the tech tree regardless of whether or not they are
        researched in no particular order
        """
        ...

    def researched_techs(self) -> list[str]:
        ...

    def is_researched(self, tech_name: str) -> bool:
        ...

    def research(self, tech_name: str) -> bool:
        ...

    def tech_info(self, tech_name: str) -> TechInfo | None:
        """
        Returns a TechInfo object about the tech with the given name if the tech is found in the tree.
        Returns None if the tech isn't found
        """
        ...

    def score(self) -> int:
        """
        Returns the total score of the tree. This is done by summing the point values of all of the techs
        that are researched
        """
        ...