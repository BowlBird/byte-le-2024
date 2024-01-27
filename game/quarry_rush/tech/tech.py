from typing import Callable
from game.quarry_rush.avatar.avatar_functions import AvatarFunctions


class Tech:
    """
    This class represents a single tech. It contains the name, cost, point value, and effect
    of researching the tech
    """

    def __init__(self, name: str, cost: int, point_value: int, apply: Callable[[], None]):
        self.name = name
        self.cost = cost
        self.point_value = point_value
        self.apply = apply


class TechInfo:
    """
    This class contains information about a tech. It is basically Tech without the effect
    of researching the tech
    """

    def __init__(self, name: str, cost: int, point_value: int):
        self.name = name
        self.cost = cost
        self.point_value = point_value


def techs(avatar_functions: AvatarFunctions) -> dict[str, Tech]:
    ...
