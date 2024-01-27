import numpy as np
from game.common.enums import ObjectType
class utilities():
    def create_map(world):
        map = []
        for tile in world:
            if tile.is_occupied_by_object_type(ObjectType.ORE_OCCUPIABLE_STATION):
                map.append(tile)
            return map
    # Convert the world grid to a graph
    def convert_2d_to_graph(array2d):
        pass

    
        
        pass
