import random
import numpy
from game.client.user_client import UserClient
from game.common.enums import *
from game.utils.vector import Vector
from game.common.map.tile import Tile

class State(Enum):
    O_CENTER = auto() # Goes to center, mines vauluable, mines ainchent tech
    O_MINE = auto()
    O_SELL = auto() # pathfind back to home position
    O_UPGRADE = auto()
    M_CENTER = auto() # Goes to center,
    M_MINE = auto() # Mine Valuable
    M_SELL = auto()
    M_UPGRADE = auto()
    E_CENTER = auto() # Goes to center, mines vauluable, mines ainchent tech
    E_MINE = auto()
    E_SELL = auto()
    E_UPGRADE = auto()
    E_EMP = auto()

class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'JOEEEEEE BIDEEEN'
    
    
   
    
    def find_ores(self,world,pos):
        ore_tiles = []
        for i, row in enumerate(world):
            for y, tile in enumerate(row):
                if tile.get_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION):
                    o = tile.occupied_by.occupied_by
                    oh = tile.occupied_by.held_item
                    print(o, " ", oh, "\n")
                    if(o is not ObjectType.AVATAR and 
                        o is not ObjectType.EMP and
                        o is not ObjectType.LANDMINE and
                        o is not ObjectType.DYNAMITE and
                        ((oh is ObjectType.TURITE) or
                        (oh is ObjectType.COPIUM) or
                        (oh is ObjectType.LAMBDIUM) or
                        (oh is ObjectType.ANCIENT_TECH))):
                        ore_tiles.append((tile,(i,y)))
                    print(ore_tiles)
                
        distances = list(map(lambda x: numpy.sqrt((pos[0] - x[1][0])**2 + (pos[1] - x[1][1])**2), ore_tiles))
        new_tiles = list(zip(ore_tiles,distances))
        new_tiles = sorted(new_tiles, key=lambda x: x[1])
        # Tile Object, Position, Distance
        new_tiles = list(map(lambda x: (x[0][0], x[0][1], x[1]), new_tiles))
        return new_tiles

    
    def first_turn_init(self, world, avatar):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn
        """
        self.company = avatar.company
        self.my_station_type = ObjectType.TURING_STATION if self.company == Company.TURING else ObjectType.CHURCH_STATION
        self.current_state = State.O_CENTER
        self.base_position = world.get_objects(self.my_station_type)[0][0]
        self.middle = (7,3) if self.company == Company.TURING else (6, 9)
        self.valuable = ObjectType.TURITE if self.company == Company.TURING else ObjectType.LAMBDIUM

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions, world, avatar):
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you will add effort allocations or decrees to.
        :param world:       Generic world information
        """
        if turn == 1:
            self.first_turn_init(world, avatar)

        current_tile = world.game_map[avatar.position.y][avatar.position.x] # set current tile to the tile that I'm standing on
        
       

        match(self.current_state):
            case State.O_CENTER:
                # Move to middle
                # Mine nearest Vauluable
                # End condition: Full Inventory, Enough for next Upgrade
                actions = self.generate_moves(avatar, world, self.middle)
                if((avatar.position.x, avatar.position.y) == self.middle):
                    self.current_state = State.O_MINE
            case State.O_MINE:
                # Find nearest Valuable
                # if none near, mine copium
                nearby_ores = self.find_ores(world.game_map, (avatar.position.x, avatar.position.y))
                close_ores_sorted = list(filter(lambda x: x[2] < 5 and x[0] is self.valuable or x[0] is ObjectType.ANCIENT_TECH, nearby_ores))
                if(int(len(close_ores_sorted)) != 0):
                    if(close_ores_sorted[0][2] == 0):
                        print("Mining")
                        actions.append(ActionType.MINE)
                    else:
                        print("Moving")
                        actions = self.generate_moves(avatar, world, close_ores_sorted[0][1])
                else:
                    if(int(nearby_ores[0][2]) == 0):
                        print("Mining")
                        print(len(nearby_ores), "\n\n\n")
                        actions.append(ActionType.MINE)
                    else:
                        print("Moving")
                        actions = self.generate_moves(avatar, world, nearby_ores[0][1])

            case State.O_SELL:
                # Move to starting position
                # Sell
                # End condition: Enough for next upgrade -> Upgrade
                # Else -> O_Mine
                pass
            case State.O_UPGRADE:
                # Buy Improved Mining if have -> O_MINE
                # Buy Dynamite -> M_SELL
                pass
        

        return actions

    def generate_moves(self, avatar, world, end_position):
        adjacency_list = generate_adjacency_list(world.game_map)
        move_list = Graph(adjacency_list).a_star_algorithm((avatar.position.x, avatar.position.y), end_position)
        copied_move_list = move_list.copy()
        copied_move_list.insert(0, (avatar.position.x, avatar.position.y))
        zipped_moves = list(map(lambda x: (x[1][0] - x[0][0], x[1][1] - x[0][1]), zip(move_list, copied_move_list)))
        actions = []

        for move in zipped_moves:
            if move == (0, 1):
                actions.append(ActionType.MOVE_UP)

            if move == (1, 0):
                actions.append(ActionType.MOVE_LEFT)

            if move == (0, -1):
                actions.append(ActionType.MOVE_DOWN)

            if move == (-1, 0):
                actions.append(ActionType.MOVE_RIGHT)

        return actions
    
    def get_my_inventory(self, world):
        return world.inventory_manager.get_inventory(self.company)

    def generate_moves_astar(self, world, start_position, end_position):
        # Worldmap is a 2d Array
        a_star = AStar(world.game_map)

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def generate_adjacency_list(obstacles: list[list[Tile]]):
    adj = {}

    for y in range(14):
        for x in range(14):
            temp = []
            if x - 1 >= 0:
                weight = 1
                obstacle = obstacles[y][x]
                if obstacle.is_occupied_by_object_type(ObjectType.WALL) or obstacle.is_occupied_by_object_type(ObjectType.LANDMINE):
                    weight = 100000

                temp.append(((x - 1,y),weight))
            if x + 1 < 100:
                weight = 1
                obstacle = obstacles[y][x]
                if obstacle.is_occupied_by_object_type(ObjectType.WALL) or obstacle.is_occupied_by_object_type(ObjectType.LANDMINE):
                    weight = 100000

                temp.append(((x + 1,y),weight))
            if y - 1 >= 0:
                weight = 1
                obstacle = obstacles[y][x]
                if obstacle.is_occupied_by_object_type(ObjectType.WALL) or obstacle.is_occupied_by_object_type(ObjectType.LANDMINE):
                    weight = 100000
                temp.append(((x,y - 1), weight))
            if y + 1 < 100:
                weight = 1
                obstacle = obstacles[y][x]
                if obstacle.is_occupied_by_object_type(ObjectType.WALL) or obstacle.is_occupied_by_object_type(ObjectType.LANDMINE):
                    weight = 100000
                temp.append(((x,y + 1), weight))
            adj[(x,y)] = temp
    return adj

class Graph:
    # example of adjacency list (or rather map)
    # adjacency_list = {
    # 'A': [('B', 1), ('C', 3), ('D', 7)],
    # 'B': [('D', 5)],
    # 'C': [('D', 12)]
    # }

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def a_star_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + 1 < g[n] + 1:
                    n = v

            if n == None:
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                return reconst_path

            # for all neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)
        return None
    
