from typing import Self

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.station.company_station import ChurchStation, TuringStation


class Tile(Occupiable):
    """
    `Tile Class Notes:`

        The Tile class exists to encapsulate all objects that could be placed on the gameboard.

        Tiles will represent things like the floor in the game. They inherit from Occupiable, which allows for tiles to
        have certain GameObjects and the avatar on it.

        If the game being developed requires different tiles with special properties, future classes may be added and
        inherit from this class.
    """

    def __init__(self, occupied_by: GameObject = None):
        super().__init__(occupied_by)
        self.object_type: ObjectType = ObjectType.TILE