# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if action == 'Stop':
            return -100

        foodList = newFood.asList()
        minFoodDist = 1
        if foodList:
            minFoodDist = min(util.manhattanDistance(newPos, food) 
            for food in foodList)

        pelletList = successorGameState.getCapsules()
        minPelletDist = 1
        if pelletList:
            minPelletDist = min(util.manhattanDistance(newPos, pellet) 
            for pellet in pelletList)

        nearestGhost = 0
        for ghost in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost)
            if distance <= 1:
                nearestGhost += 1

        result = successorGameState.getScore()
        result += 1 /float(minFoodDist)
        result += 1 /float(minPelletDist)
        result += -100 * nearestGhost
        return result

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(agentIndex, depth, gameState):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                depth += 1

            if agentIndex == 0:
                return max(minimax(nextAgent, depth, 
                  gameState.generateSuccessor(agentIndex, nextAction)) for nextAction in actions)
            else: 
                return min(minimax(nextAgent, depth, 
                  gameState.generateSuccessor(agentIndex, nextAction)) for nextAction in actions)

        maximum = float("-inf")
        depth = 0
        for action in gameState.getLegalActions(0):
            value = minimax(1, depth, gameState.generateSuccessor(0, action))
            if value > maximum:
                maximum = value
                bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def prunedMinimax(agentIndex, depth, gameState, alpha, beta):
            "Check if max depth, win or loss"
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1

            "Resets agent indexing and increases depth after all agents take turns"
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                depth += 1

            "Pacman"
            if agentIndex == 0:
                v = float("-inf")
                "Loop through successors to find max value"
                for nextAction in actions:
                    successor = gameState.generateSuccessor(agentIndex, nextAction)
                    v = max(v, prunedMinimax(nextAgent, depth, successor, alpha, beta))
                    "value is greater than beta pacman won't allow it to be bata, prune"
                    if v > beta:
                        return v
                    alpha = max(alpha, v)
                return v
            else:
                v = float("inf")
                "Loop through successors to find min value"
                for nextAction in actions:
                    successor = gameState.generateSuccessor(agentIndex, nextAction)
                    v = min(v, prunedMinimax(nextAgent, depth, successor, alpha, beta))
                    "value is less than alpha ghost won't allow it to be alpha, prune"
                    if v < alpha:
                        return v
                    "update beta"
                    beta = min(beta, v)
                return v
                
        alpha = float("-inf")
        beta = float("inf")
        depth = 0
        for action in gameState.getLegalActions(0):
            value = prunedMinimax(1, depth, gameState.generateSuccessor(0, action), alpha, beta)
            if value > alpha:
                alpha = value
                bestAction = action
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def expectimax(agentIndex, depth, gameState):
            "Check if max depth, win or loss"
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1

            "reset agent index once all have taken turns"
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                depth += 1

            "pacman"
            if agentIndex == 0:
                v = float("-inf")
                "Loop through successors to find max value"
                for nextAction in actions:
                    successor = gameState.generateSuccessor(agentIndex, nextAction)
                    "return max value for pacman"
                    v = max(v, expectimax(nextAgent, depth, successor))
                return v
            else: 
                "ghosts"
                v = 0
                successorSum = 0
                numSuccessors = 0
                "Loop through successors to find average value"
                for nextAction in actions:
                    successor = gameState.generateSuccessor(agentIndex, nextAction)
                    successorSum += expectimax(nextAgent, depth, successor)
                    numSuccessors += 1
                "return the average of the successors"
                v = (successorSum / numSuccessors)
                return v
 
        maximum = float("-inf")
        depth = 0
        for action in gameState.getLegalActions(0):
            value = expectimax(1, depth, gameState.generateSuccessor(0, action))
            if value > maximum:
                maximum = value
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    """get all the food, and find the closest food to pacman"""
    foodList = newFood.asList()
    minFoodDist = -1
    if foodList:
        minFoodDist = min(util.manhattanDistance(newPos, food) 
        for food in foodList)

    """find the closest ghost to pacman"""
    proximityToGhost = 0
    for ghost in currentGameState.getGhostPositions():
        distance = util.manhattanDistance(newPos, ghost)
        if distance <= 1:
            proximityToGhost += 1

    """ get the number of capsules available
    We want to make sure pacman goes towards capsules to 
    increase the score, so remaining capsules are bad"""
    totalCapsules = len(currentGameState.getCapsules())

    """basic state score"""
    result = currentGameState.getScore() 
    """want to go towards food"""
    result += 1 / float(minFoodDist) 
    """proximity to ghost is bad"""
    result -= proximityToGhost
    """want to collect capsules"""
    result -= totalCapsules
    return result

# Abbreviation
better = betterEvaluationFunction
