import random
from game.common.enums import ObjectType, Company
from game.common.game_object import GameObject
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.entity.ores import Lambdium, Turite, Copium
from game.utils.vector import Vector
from game.common.map.tile import Tile
from game.common.avatar import Avatar
from typing import Self


class OreOccupiableStation(OccupiableStation):
    """
    Station that holds the different types of ores; inherits from OccupiableStation.
    """

    def __init__(self, position: Vector = Vector(0, 0), seed: float = 0, special_weight: float = .2,
                 ancient_tech_weight: float = .1):
        super().__init__(held_item=Copium())
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION
        self.seed = seed
        self.position = position
        self.rand = random.Random((19 * position.x + 23 * position.y) * seed)
        self.special_weight = special_weight
        self.ancient_tech_weight = ancient_tech_weight
        self.held_item = Copium()

    def give_item(self, company: Company, inventory_manager: InventoryManager = None, drop_rate: int = 1) -> None:
        ...

    def remove_from_game_board(self, tile: Tile):
        ...
    
    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager):
        ...