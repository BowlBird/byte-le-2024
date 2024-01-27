from game.utils.vector import Vector
from game.common.stations.occupiable_station import OccupiableStation
from game.common.enums import *
from typing import Self


class Dynamite(OccupiableStation):
    """
    Dynamite is a class that represents the dynamite an Avatar can place on the ground. It inherits from Occupiable
    Station to permit Avatar instances to walk on them.
    """
    def __init__(self, position: Vector | None = None, blast_radius: int = 0, company: Company = Company.CHURCH):
        super().__init__()
        self.position: Vector | None = position
        self.blast_radius: int = blast_radius
        self.fuse: int = 3  # how many turns it'll take before the dynamite explodes
        self.object_type: ObjectType = ObjectType.DYNAMITE
        self.company: Company = company

        # property to be used for the visualizer mainly; will have a separate method for other uses in gameboard
        self.can_explode = False

    # position getter
    @property
    def position(self) -> Vector | None:
        return self.__position

    # position setter
    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None.')
        self.__position: Vector | None = position

    # blast radius getter
    @property
    def blast_radius(self) -> int:
        return self.__blast_radius

    # blast radius setter
    @blast_radius.setter
    def blast_radius(self, blast_radius: int) -> None:
        if blast_radius is None or not isinstance(blast_radius, int):
            raise ValueError(f'{self.__class__.__name__}.blast_radius must be an int.')
        self.__blast_radius: int = blast_radius

    # can_explode getter
    @property
    def can_explode(self) -> bool:
        return self.__can_explode

    # can_explode setter
    @can_explode.setter
    def can_explode(self, can_explode: bool) -> None:
        if can_explode is None or not isinstance(can_explode, int):
            raise ValueError(f'{self.__class__.__name__}.can_explode must be a bool.')
        self.__can_explode = can_explode

    # company gettter
    @property
    def company(self) -> Company:
        return self.__company

    # company setter
    @company.setter
    def company(self, company: Company) -> None:
        if company is None or not isinstance(company, Company):
            raise ValueError(f'{self.__class__.__name__}.company must be a Company enum.')
        self.__company = company


    def decrement_fuse(self) -> None:
        ...

    def is_fuse_at_0(self) -> bool:
        ...

    # detonate method
    def detonate(self):
        ...