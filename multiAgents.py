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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # score = successorGameState.getScore()
        # min_dist = min([manhattanDistance(newPos, pos) for pos in newFood.asList()])

        # print((1 / len(newFood.asList())) * min_dist)
        # return (1 / len(newFood.asList())) * min_dist 

        if len(newFood.asList()) == 0:
            dist_to_food = 1000000 
        else:
            dist_to_food = min([manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()])
        
        closest_ghost = min([manhattanDistance(newPos, ghostPos) for ghostPos in successorGameState.getGhostPositions()])

        if any(newScaredTimes):
            return successorGameState.getScore() + (1 / dist_to_food)
        else:
            return successorGameState.getScore() + 0.01 * closest_ghost + (1 / dist_to_food)

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        def value(agentIndex, state, depth):
            if depth >= self.depth:
                return self.evaluationFunction(state)
            if agentIndex >= state.getNumAgents():
                agentIndex = 0
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                return max_val(agentIndex, state, depth)
            else:
                return min_val(agentIndex, state, depth)

        def max_val(agentIndex, state, depth):
            v = float("-inf")
            for action in state.getLegalActions(agentIndex):
                succ = state.generateSuccessor(agentIndex, action)
                v = max(v, value(agentIndex + 1, succ, depth))
            return v

        def min_val(agentIndex, state, depth):
            v = float("inf")
            if agentIndex == state.getNumAgents() - 1:
                depth += 1
            for action in state.getLegalActions(agentIndex):
                succ = state.generateSuccessor(agentIndex, action)
                v = min(v, value(agentIndex + 1, succ, depth))
            return v
        
        bestMove = None
        bestMoveVal = float("-inf")

        if gameState.isWin() or gameState.isLose():
                return bestMove

        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            val = value(agentIndex = 1, state = succ, depth = 0)
            if val > bestMoveVal:
                bestMove = action
                bestMoveVal = val
        return bestMove



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def value(agentIndex, state, depth, alpha, beta):
            if depth >= self.depth:
                return self.evaluationFunction(state)
            if agentIndex >= state.getNumAgents():
                agentIndex = 0
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                return max_val(agentIndex, state, depth, alpha, beta)
            else:
                return min_val(agentIndex, state, depth, alpha, beta)

        def max_val(agentIndex, state, depth, alpha, beta):
            v = float("-inf")
            for action in state.getLegalActions(agentIndex):
                succ = state.generateSuccessor(agentIndex, action)
                v = max(v, value(agentIndex + 1, succ, depth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_val(agentIndex, state, depth, alpha, beta):
            v = float("inf")
            if agentIndex == state.getNumAgents() - 1:
                depth += 1
            for action in state.getLegalActions(agentIndex):
                succ = state.generateSuccessor(agentIndex, action)
                v = min(v, value(agentIndex + 1, succ, depth, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        
        bestMove = None
        bestMoveVal = float("-inf")

        if gameState.isWin() or gameState.isLose():
                return bestMove

        a = float("-inf")
        b = float("inf")

        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            val = value(agentIndex = 1, state = succ, depth = 0, alpha = a, beta = b)
            if val > bestMoveVal:
                bestMove = action
                bestMoveVal = val
            a = max(val, a)
        return bestMove



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        def mean(lst):
            return sum(lst) / len(lst)
        
        def value(agentIndex, state, depth):
            if depth >= self.depth:
                return self.evaluationFunction(state)
            if agentIndex >= state.getNumAgents():
                agentIndex = 0
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                return max_val(agentIndex, state, depth)
            else:
                return min_val(agentIndex, state, depth)

        def max_val(agentIndex, state, depth):
            v = float("-inf")
            # state_vals = []
            for action in state.getLegalActions(agentIndex):
                succ = state.generateSuccessor(agentIndex, action)
                v = max(v, value(agentIndex + 1, succ, depth))
                # state_val = value(agentIndex + 1, succ, depth)
                # state_vals.append(state_val)
            # v = mean(state_vals)
            return v

        def min_val(agentIndex, state, depth):
            # v = float("inf")
            state_vals = []
            if agentIndex == state.getNumAgents() - 1:
                depth += 1
            
            for action in state.getLegalActions(agentIndex):
                succ = state.generateSuccessor(agentIndex, action)
                state_val = value(agentIndex + 1, succ, depth)
                state_vals.append(state_val)
            v = mean(state_vals)
            return v
        
        bestMove = None
        bestMoveVal = float("-inf")

        if gameState.isWin() or gameState.isLose():
                return bestMove

        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            val = value(agentIndex = 1, state = succ, depth = 0)
            if val > bestMoveVal:
                bestMove = action
                bestMoveVal = val
        return bestMove


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # score = successorGameState.getScore()
    # min_dist = min([manhattanDistance(newPos, pos) for pos in newFood.asList()])

    # print((1 / len(newFood.asList())) * min_dist)
    # return (1 / len(newFood.asList())) * min_dist 

    if len(newFood.asList()) == 0:
        dist_to_food = 1000000 
    else:
        dist_to_food = min([manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()])
    
    closest_ghost = min([manhattanDistance(newPos, ghostPos) for ghostPos in currentGameState.getGhostPositions()])

    if any(newScaredTimes):
        return (currentGameState.getScore()) + (1 / dist_to_food) + (1 / closest_ghost)
    else:
        return (currentGameState.getScore()) + 0.01 * closest_ghost + (1 / dist_to_food)

# Abbreviation
better = betterEvaluationFunction