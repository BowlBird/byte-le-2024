import random

from game.client.user_client import UserClient
from game.common.enums import *
from game.utils.vector import Vector

class State(Enum):
    MINING = auto()
    SELLING = auto()


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Unpaid Intern'
    
    def has_goodies(tile):
         if (tile.occupied_by):
            return True
         else:
            return False
    
    def first_turn_init(self, world, avatar):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn
        """
        self.company = avatar.company
        self.my_station_type = ObjectType.TURING_STATION if self.company == Company.TURING else ObjectType.CHURCH_STATION
        self.current_state = State.MINING
        self.base_position = world.get_objects(self.my_station_type)[0][0]
        print("printing goodies")
        goodies_list = filter(self.has_goodies, world.get_objects(ObjectType.OCCUPIABLE_STATION))
        print(goodies_list)
        # for tile in goodies_list:
        #     print("here!")
        #     print(tile.occupied_by)       
        # Attempted to generate a path between the two points. THIS IS DEBUG RN
        self.generate_moves_astar(world, Vector(0, 0), Vector(1, 1))

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
        
        # If I start the turn on my station, I should...
        if current_tile.occupied_by.object_type == self.my_station_type:
            # buy Improved Mining tech if I can...
            if avatar.science_points >= avatar.get_tech_info('Improved Drivetrain').cost and not avatar.is_researched('Improved Drivetrain'):
                return [ActionType.BUY_IMPROVED_DRIVETRAIN]
            # otherwise set my state to mining
            self.current_state = State.MINING
            
        # If I have at least 5 items in my inventory, set my state to selling
        if len([item for item in self.get_my_inventory(world) if item is not None]) >= 5:
            self.current_state = State.SELLING
            
        # Make action decision for this turn
        if self.current_state == State.SELLING:
            # actions = [ActionType.MOVE_LEFT if self.company == Company.TURING else ActionType.MOVE_RIGHT] # If I'm selling, move towards my base
            actions = self.generate_moves(avatar.position, self.base_position, turn % 2 == 0)
        else:
            if current_tile.occupied_by.object_type == ObjectType.ORE_OCCUPIABLE_STATION:
                # If I'm mining and I'm standing on an ore, mine it
                actions = [ActionType.MINE]
            else:
                # If I'm mining and I'm not standing on an ore, move randomly
                actions = [random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_DOWN])]
                
        return actions

    def generate_moves(self, start_position, end_position, vertical_first):
        """
        This function will generate a path between the start and end position. It does not consider walls and will
        try to walk directly to the end position.
        :param start_position:      Position to start at
        :param end_position:        Position to get to
        :param vertical_first:      True if the path should be vertical first, False if the path should be horizontal first
        :return:                    Path represented as a list of ActionType
        """
        dx = end_position.x - start_position.x
        dy = end_position.y - start_position.y
        
        horizontal = [ActionType.MOVE_LEFT] * -dx if dx < 0 else [ActionType.MOVE_RIGHT] * dx
        vertical = [ActionType.MOVE_UP] * -dy if dy < 0 else [ActionType.MOVE_DOWN] * dy
        
        return vertical + horizontal if vertical_first else horizontal + vertical

    def get_my_inventory(self, world):
        return world.inventory_manager.get_inventory(self.company)

    def generate_moves_astar(self, world, start_position, end_position):
        # Worldmap is a 2d Array
        a_star = AStar(world.game_map)

# Weighted Graph Stuff
class weighted_graph:
    def __init__(self):
        graph = {}
        vertices_no = 0

    # Constructs the graph given a 2d array of tile object
    def construct_from_grid(self, grid):
        for y in grid:
            for x in y:
                self.add_vertex(x)

        #print(graph)
        
        for col in range(14):
            for row in range(14):
                print(col, " ", row)
                current_pos = col * 14 + row
                # Left
                # self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 
                # Right
                # self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) 
                # Up
                # self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col-1) * 14) + row), 1) 
                # Down
                # self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 

                if(col == 0):
                    if(row == 0):
                        #Top Left
                        # Only do Right and Down
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) # Right
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 

                    elif(row == 13):
                        # Top Right
                        # Do Left Down
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 

                    else:
                        # First Row
                        # Do Left Right and Down
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 
                elif(col == 13):
                    if(row == 0):
                        #UP, Right
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col-1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) 

                    elif(row == 13):
                        #Up, LEft
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col-1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 
                    else:
                        #Left Right Up
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) 
                else:
                    if(row == 0):
                        # Up Down Right
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col-1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) 

                    elif(row == 13):
                        #UP Down Left
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col-1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 

                    else:
                        #Up Down Left Right
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col-1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, ((col+1) * 14) + row), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos - 1), 1) 
                        self.add_edge(self.get_nth_key(graph, current_pos), self.get_nth_key(graph, current_pos + 1), 1) 

    def add_vertex(self, v):
        global graph
        global vertices_no
        if v in graph:
            print("Vertex ", v, " already exists.")
        else:
            vertices_no = vertices_no + 1
            graph[v] = []

        # Add an edge between vertex v1 and v2 with edge weight e
    def add_edge(self, v1, v2, e):
        global graph
        # Check if vertex v1 is a valid vertex
        if v1 not in graph:
            print("Vertex ", v1, " does not exist.")
        # Check if vertex v2 is a valid vertex
        elif v2 not in graph:
            print("Vertex ", v2, " does not exist.")
        else:
            # Since this code is not restricted to a directed or 
            # an undirected graph, an edge between v1 v2 does not
            # imply that an edge exists between v2 and v1
            temp = [v2, e]
            graph[v1].append(temp)

    # Print the graph
    def print_graph(self):
        global graph
        for vertex in graph:
            for edges in graph[vertex]:
                print(vertex, " -> ", edges[0], " edge weight: ", edges[1])

    def get_nth_key(self, dictionary, n=0):
        if n < 0:
            n += len(dictionary)
        for i, key in enumerate(dictionary.keys()):
            if i == n:
                return key
        raise IndexError("dictionary index out of range") 

# ASTAR STUFF
graph = {}
vertices_no = 0

#Convert grid2d to graph
class AStar:
    def __init__(self, grid):
        graph = {}
        weighted = weighted_graph()
        weighted.construct_from_grid(grid)
        weighted.print_graph()
