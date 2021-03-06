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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        MAX_VALUE = float("inf")

        if min(manhattanDistance(newPos, ghost) for ghost in successorGameState.getGhostPositions()) < 2:
            return -MAX_VALUE
        if len(newFood.asList()) == 0:
            return MAX_VALUE

        nearestFoodDistance = min(manhattanDistance(newPos, food) for food in newFood.asList())

        return successorGameState.getScore() + (10.0 / nearestFoodDistance)

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        gameState.getNumAgents():ge
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # returns first index of move tuple which is the action
        return self.getMax(gameState, 0, 0)[0]

    # this function gets called between each getMax and getMin to control
    # the depth and agent's index
    # also returns the evaluation for leaf nodes
    def miniMax(self, gameState, agentIndex, depth):
        if (agentIndex + 1 == gameState.getNumAgents() and depth + 1 == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex + 1 == gameState.getNumAgents():
            return self.getMax(gameState, 0, depth + 1)[1]
        else:
            return self.getMin(gameState, agentIndex + 1, depth)[1]

    def getMax(self, gameState, agentIndex, depth):
        bestMove = ("null", -float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            evaluation = (action, self.miniMax(gameState.generateSuccessor(agentIndex, action), agentIndex, depth))
            bestMove = max(bestMove, evaluation, key=lambda tup: tup[1])
        return bestMove

    def getMin(self, gameState, agentIndex, depth):
        bestMove = ("null", float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            evaluation = (action, self.miniMax(gameState.generateSuccessor(agentIndex, action), agentIndex, depth))
            bestMove = min(bestMove, evaluation, key=lambda tup: tup[1])
        return bestMove


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.getMax(gameState, 0, 0, -float("inf"), float("inf"))[0]

    def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        if (agentIndex + 1 == gameState.getNumAgents() and depth + 1 == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex + 1 == gameState.getNumAgents():
            return self.getMax(gameState, 0, depth + 1, alpha, beta)[1]
        else:
            return self.getMin(gameState, agentIndex + 1, depth, alpha, beta)[1]

    def getMax(self, gameState, agentIndex, depth, alpha, beta):
        bestMove = ("null", -float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            evaluation = (action, self.alphaBeta(gameState.generateSuccessor(agentIndex, action), agentIndex, depth, alpha, beta))
            bestMove = max(bestMove, evaluation, key=lambda tup: tup[1])

            if bestMove[1] > beta:
                return bestMove
            alpha = max(alpha, bestMove[1])

        return bestMove

    def getMin(self, gameState, agentIndex, depth, alpha, beta):
        bestMove = ("null", float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            evaluation = (action, self.alphaBeta(gameState.generateSuccessor(agentIndex, action), agentIndex, depth, alpha, beta))
            bestMove = min(bestMove, evaluation, key=lambda tup: tup[1])

            if bestMove[1] < alpha:
                return bestMove
            beta = min(beta, bestMove[1])

        return bestMove


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
        "*** YOUR CODE HERE ***"
        return self.getMax(gameState, 0, 0,)[0]

    def expectiMax(self, gameState, agentIndex, depth):
        if (agentIndex + 1 == gameState.getNumAgents() and depth + 1 == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex + 1 == gameState.getNumAgents():
            return self.getMax(gameState, 0, depth + 1)[1]
        else:
            return self.getChance(gameState, agentIndex + 1, depth)

    def getMax(self, gameState, agentIndex, depth):
        bestMove = ("null", -float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            evaluation = (action, self.expectiMax(gameState.generateSuccessor(agentIndex, action), agentIndex, depth))
            bestMove = max(bestMove, evaluation, key=lambda tup: tup[1])

        return bestMove

    def getChance(self, gameState, agentIndex, depth):
        chance = 0
        probability = 1.0 / len(gameState.getLegalActions(agentIndex))
        for action in gameState.getLegalActions(agentIndex):
            evaluation = (action, self.expectiMax(gameState.generateSuccessor(agentIndex, action), agentIndex, depth))
            chance += evaluation[1] * probability

        return chance


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    foodsPos = currentGameState.getFood().asList()
    numFood = currentGameState.getNumFood()
    numCapsule = len(currentGameState.getCapsules())
    ghostsPos = currentGameState.getGhostPositions()
    gameScore = currentGameState.getScore()
    evaluation = 0

    # If there is food left then no good
    evaluation += 1000000.0 / (numFood + 1)

    # If food is near then good
    if numFood != 0:
        nearestFoodDistance = min(manhattanDistance(pacmanPos, food) for food in foodsPos)
        evaluation += 1000.0 / nearestFoodDistance

    # If capsules left then no good
    evaluation += 10000.0 / (numCapsule + 1)

    # If ghost is near then no good
    if min(manhattanDistance(pacmanPos, ghost) for ghost in ghostsPos) < 2:
        evaluation -= float("inf")

    return evaluation + gameScore


# Abbreviation
better = betterEvaluationFunction
