# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os
import math
from heapq import *
import sys

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_dist(a,b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

# https://en.wikipedia.org/wiki/Taxicab_geometry
def manhattan_dist_complex_heuristic(state, problem):
        # the state includes a grid of where the food is (problem isn't ter)
        position, food_grid = state
        pacman_x, pacman_y = position

        one_fruit = False
        tiles = food_grid.as_list()
        if len(tiles) == 0:
            return 0
        elif len(tiles) == 1:
            one_fruit = True

        tiles.sort(key=lambda tile: abs(tile[0]-pacman_x) + abs(tile[1]-pacman_y))
        # tiles.reverse()
        # print(len(tiles))
        closest_fruit = tiles[0]
        closest_fruit_dist = manhattan_dist(position, closest_fruit) 
        if one_fruit:
            return closest_fruit_dist

        furthest_fruit = tiles[-1]
        furthest_fruit_dist = manhattan_dist(position, closest_fruit)

        if not one_fruit:
            second_furthest_fruit = tiles[-2]
            dist_between_furthest_fruits = manhattan_dist(furthest_fruit, second_furthest_fruit)
            dist_between_second_furthest_and_player = manhattan_dist(second_furthest_fruit, position) 
            return dist_between_furthest_fruits + dist_between_second_furthest_and_player

def euclidian_dist_closest_pellet_heuristic(state, problem):
    # Find the distance between each pellet of food
    position, food_grid = state
    pacman_x, pacman_y = position

    food_dist = 0
    tiles = food_grid.as_list()
    # print(tiles)
    if len(tiles) == 0:
        return 0
    tiles.sort(key=lambda tile: problem.precomputed['eucDist'][(position, (tile[0],tile[1]))])
    closest_fruit = tiles[0]


    return problem.precomputed['eucDist'][(position, (closest_fruit[0],closest_fruit[1]))] * 1.001

def near_far_heuristic(state, problem):
    # Find the distance between each pellet of food
    position, food_grid = state
    pacman_x, pacman_y = position

    food_dist = 0
    tiles = food_grid.as_list()
    # print(tiles)
    if len(tiles) == 0:
        return 0
    tiles.sort(key=lambda tile: problem.precomputed['manDist'][(position, (tile[0],tile[1]))])


    closest_fruit = tiles[0]
    furthest_fruit = tiles[len(tiles)-1]

    if closest_fruit == furthest_fruit:
        return 0

    return problem.precomputed['manDist'][(position, (closest_fruit[0],closest_fruit[1]))] + problem.precomputed['manDist'][((closest_fruit[0],closest_fruit[1]), (furthest_fruit[0],furthest_fruit[1]))] 


def euclidian_dist_complex_furthest_pellet_heuristic(state, problem):
    # Find the distance between each pellet of food
    position, food_grid = state
    pacman_x, pacman_y = position

    food_dist = 0
    tiles = food_grid.as_list()
    # print(tiles)
    if len(tiles) == 0:
        return 0
    tiles.sort(key=lambda tile: problem.precomputed['manDist'][(position, (tile[0],tile[1]))])
    # print(tiles)
    # print(food_dist)

    # Find farthest and second farthest
    furthest_fruit = None
    second_furthest_fruit = None
    for i in range(len(tiles)-1, 0):
        if(tiles[i]):
            if not furthest_fruit:
                furthest_fruit = tiles[i]
            elif not second_furthest_fruit:
                second_furthest_fruit = tiles[i]
            else:
                break
    if furthest_fruit and second_furthest_fruit:
        dist_furthest_fruits = problem.precomputed['manDist'][((furthest_fruit[0],furthest_fruit[1]), (second_furthest_fruit[0],second_furthest_fruit[1]))]
        pacman_dist_second_furthest = problem.precomputed['manDist'][(position, (furthest_fruit[0],furthest_fruit[1]))] 
        h = dist_furthest_fruits + pacman_dist_second_furthest 
    elif furthest_fruit:
        h = problem.precomputed['manDist'][(position, (furthest_fruit[0],furthest_fruit[1]))]
    else:
        h = 0
    return h 

def euclidian_dist_each_pellet_heuristic(state, problem):
    # Find the distance between each pellet of food
    position, food_grid = state
    pacman_x, pacman_y = position

    food_dist = 0

    for x in range(0, food_grid.width):
        for y in range(0, food_grid.height):
            if(food_grid[x][y]):
                food_dist += problem.precomputed['eucDist'][(position, (x,y))]
    # print(food_dist)
    return food_dist * (1.001)

def greedy_heuristic(state, problem):
    position, food_grid = state
    pacman_x, pacman_y = position

    tiles = food_grid.as_list()
    if len(tiles) == 0:
        return 0

    tiles.sort(key=lambda tile: abs(tile[0]-pacman_x) + abs(tile[1]-pacman_y))
    # tiles.reverse()
    # print(len(tiles))
    closest_fruit = tiles[0]
    closest_fruit_dist = manhattan_dist(position, closest_fruit) 

    return closest_fruit_dist


def waypoint_heuristic(state, problem):
    pass

def graph_search_heurisitc():
    pass



def heuristic(state, problem=None):
    from search_agents import FoodSearchProblem
    
    # 
    # heuristic for the find-the-goal problem
    # 
    if isinstance(problem, SearchProblem):
        return 0

    # traveling-salesman problem (collect multiple food pellets)
    # 
    # Note: The actual end "goal" of food search is all pieces of food have been eaten
    # it is not that the closest food has been consumed
    elif isinstance(problem, FoodSearchProblem):
        if(problem.precomputed['heuristic'] == 'manhattan_dist_complex_heuristic'):
            return manhattan_dist_complex_heuristic(state, problem)
        elif(problem.precomputed['heuristic'] == 'euclidian_dist_each_pellet_heuristic'):
            return 10*euclidian_dist_each_pellet_heuristic(state, problem) + 4*near_far_heuristic(state, problem) + 2*greedy_heuristic(state, problem)
        elif(problem.precomputed['heuristic'] == 'greedy_heuristic'):
            return greedy_heuristic(state, problem)
        elif(problem.precomputed['heuristic'] == 'euclidian_dist_closest_pellet_heuristic'):
            return euclidian_dist_closest_pellet_heuristic(state, problem)
        elif(problem.precomputed['heuristic'] == 'euclidian_dist_complex_furthest_pellet_heuristic'):
            return euclidian_dist_complex_furthest_pellet_heuristic(state, problem)
        elif(problem.precomputed['heuristic'] == 'near_far_heuristic'):
            return near_far_heuristic(state, problem)
        else:
            return 0 

class Node():
    def __init__(self, parent, state, action, g, h):
        self.parent = parent
        self.state = state
        self.action = action
        self.g = g
        self.f = g + h

    def _cmpkey(self):
        return self.f

    def _compare(self, other, method):
        try:
            return method(self._cmpkey(), other._cmpkey())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other".
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)



class AStar():
    def __init__(self, problem, heuristic):
        self.problem = problem
        self.heuristic = heuristic
        self.problem.precomputed = {}

    # Returns solution node, or -1 (failure)
    def search(self):
        ## Set up A* search
        start_state = self.problem.get_start_state()

        rootNode = Node(parent=None, state=start_state, action=None, g=0, h=self.heuristic(start_state, self.problem))
        frontier = [] # Heap queue (Priority queue)
        heappush(frontier, rootNode)
        reached = {start_state: rootNode} # Lookup table
        
        while len(frontier) > 0:
            node = heappop(frontier)
            if(self.problem.is_goal_state(node.state)): return node

            for child in self.problem.get_successors(node.state):

                cs = child.state
                h = self.heuristic(cs, self.problem)
                childNode = Node(parent=node, state=cs, action=child.action, g=node.g+child.cost, h=h)
                if cs not in reached or childNode.f < reached[cs].f:
                    reached[cs] = childNode
                    heappush(frontier, childNode)

        return -1

    # Constructs precomputed data based on heuristic and constructs solution array
    def execute(self):
        
        # self.problem.precomputed['heuristic'] = 'euclidian_dist_each_pellet_heuristic'
        # heuristic = 'greedy_heuristic'
        # euclidian_dist_closest_pellet_heuristic
        from search_agents import FoodSearchProblem

        if isinstance(self.problem, FoodSearchProblem):
            self.problem.precomputed['heuristic'] = 'euclidian_dist_each_pellet_heuristic'

            self.problem.precomputed['eucDist'] = {} # Query with (point1, point2)
            self.problem.precomputed['manDist'] = {}
            position, food_grid = self.problem.get_start_state()
            tempArr = []
            for x in range(0, food_grid.width):
                for y in range(0, food_grid.height):
                    tempArr.append((x, y))

            for coordOne in tempArr:
                for coordTwo in tempArr:
                    if(coordOne != coordTwo):
                        self.problem.precomputed['eucDist'][(coordOne, coordTwo)] = euclidean_dist(coordOne, coordTwo)
                        self.problem.precomputed['manDist'][(coordOne, coordTwo)] = manhattan_dist(coordOne, coordTwo)



        
        solutionNode = self.search()

        if(solutionNode == -1):
            print('SOLUTION NOT FOUND. EXITING')
            sys.exit()

        path = []

        node = solutionNode
        while node.parent is not None:
            path.append(node.action)
            node = node.parent

        path.reverse()
        return path

def a_star_search(problem, heuristic=heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # What does this function need to return?
    #     list of actions that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    
    # start_state = problem.get_start_state()
    # print(start_state)
    # transitions = problem.get_successors(start_state)
    # print(transitions[0].cost)
    # example_path = [  transitions[0].action  ]
    # path_cost = problem.get_cost_of_actions(example_path)
    # return example_path
    #
   
    astar = AStar(problem, heuristic)
    solution_path = astar.execute()
    # print(solution_path)
    return solution_path

    # util.raise_not_defined()


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search
