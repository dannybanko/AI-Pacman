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
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    # Search the deepest nodes in the search tree first.

    start = problem.getStartState()
    fringe = util.Stack() # keeps track of the state, visited nodes and the path
    visited = []
    directions = []

    fringe.push((start, visited, directions))

    while not fringe.isEmpty():
        state, nodesVisited, directions = fringe.pop()
        # check if in visited
        if state not in visited:
            visited += [state]

            if problem.isGoalState(state):
                return directions

            # find all successors
            for node in problem.getSuccessors(state):
                successor, nextDirection, cost = node
                fringe.push((successor, visited + [state], directions + [nextDirection]))           
    return directions

def breadthFirstSearch(problem):
    # Search the shallowest nodes in the search tree first.

    start = problem.getStartState()
    fringe = util.Queue() # keeps track of the state, visited nodes and the path
    visited = []
    directions = []

    fringe.push((start, visited, directions))

    while not fringe.isEmpty():
        state, nodesVisited, directions = fringe.pop()
        # check if in visited
        if state not in visited:
            visited += [state] 
            
            if problem.isGoalState(state):
                return directions
            
            # find all successors
            for node in problem.getSuccessors(state):
                successor, nextDirection, cost = node
                fringe.push((successor, visited + [state], directions + [nextDirection]))
    return directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    start = problem.getStartState()
    fringe = util.PriorityQueue() # keeps track of the state, path, and the total cost
    visited = []
    directions = []

    fringe.push((start, directions, 0),0)

    while not fringe.isEmpty():
        state, directions, cost = fringe.pop()
        # check if in visited
        if state not in visited:
            visited += [state]

            if problem.isGoalState(state):
                return directions

            # get all successors, and then update total cost
            for node in problem.getSuccessors(state):
                successor, nextDirection, successorCost = node
                fringe.push((successor, directions + [nextDirection], 
                cost + successorCost), cost + successorCost)
    return directions
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    start = problem.getStartState()
    fringe = util.PriorityQueue() # keeps track of the state, path, total cost, and heuristic
    visited = []
    directions = []
    initialCost = 0
    initialHeur = heuristic(start, problem) # intitial heuristic

    fringe.push((start, directions, initialCost), initialHeur)

    while not fringe.isEmpty():
        state, directions, cost = fringe.pop()
        # check if in visited
        if state not in visited:
            visited += [state]

            if problem.isGoalState(state):
                return directions
            
            # get all successors, update cost and heuristic
            for node in problem.getSuccessors(state):
                successor, nextDirection, successorCost = node
                totalCost = cost + successorCost # cost
                totalSum = totalCost + heuristic(successor, problem) # heuristic
                fringe.push((successor, directions + [nextDirection], cost + successorCost), totalSum)
    return directions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
