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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        # raise NotImplementedError("To be implemented")
        __, nextAction = self.performMinimax(0, self.index, gameState)
        return nextAction

    def performMinimax(self, depth, agentIndex, gameState):
        if (gameState.isWin() or gameState.isLose() or depth >= self.depth):
            return self.evaluationFunction(gameState), None
        
        scores = []
        isMinplayer = True if agentIndex != 0 else False
        bestScore = float("inf") if isMinplayer else float("-inf")
        legalMoves = gameState.getLegalActions(agentIndex)
        nextIndex = (agentIndex + 1) % gameState.getNumAgents() # 0 -> 1 -> 2 -> 0 -> 1 -> 2 -> ...
        
        if nextIndex == 0:
            depth +=1

        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        for move in legalMoves:
            nextState = gameState.getNextState(agentIndex, move)
            nextValue, __ = self.performMinimax(depth, nextIndex, nextState)
            bestScore = min(bestScore, nextValue) if isMinplayer else max(bestScore, nextValue)
            scores.append(nextValue)
        
        if isMinplayer:
            return bestScore, None
        else:
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            choisenIndex = random.choice(bestIndices)
            return max(scores), legalMoves[choisenIndex]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        # raise NotImplementedError("To be implemented")
        alpha, beta = float("-inf"), float("inf")
        __, nextAction = self.performAlphaBeta(0, self.index, gameState, alpha, beta)
        return nextAction

    def performAlphaBeta(self, depth, agentIndex, gameState, alpha, beta):
        if (gameState.isWin() or gameState.isLose() or depth >= self.depth):
            return self.evaluationFunction(gameState), None
        
        scores = []
        isMinplayer = True if agentIndex != 0 else False
        bestScore = float("inf") if isMinplayer else float("-inf")
        legalMoves = gameState.getLegalActions(agentIndex)
        nextIndex = (agentIndex + 1) % gameState.getNumAgents() # 0 -> 1 -> 2 -> 0 -> 1 -> 2 -> ...
        
        if nextIndex == 0:
            depth +=1
        
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        for move in legalMoves:
            nextState = gameState.getNextState(agentIndex, move)
            nextValue, __ = self.performAlphaBeta(depth, nextIndex, nextState, alpha, beta)
            bestScore = min(bestScore, nextValue) if isMinplayer else max(bestScore, nextValue)
            if isMinplayer :
                if nextValue < alpha:
                    return nextValue, None
                beta = min(beta, bestScore)
            else: 
                if nextValue > beta:
                    return nextValue, move
                alpha = max(alpha, nextValue)
            scores.append(nextValue)
        
        if isMinplayer:
            return bestScore, None
        else:
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            choisenIndex = random.choice(bestIndices)
            return max(scores), legalMoves[choisenIndex]
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        # raise NotImplementedError("To be implemented")

        __, nextAction = self.performExpectimax(0, self.index, gameState)
        return nextAction

    def performExpectimax(self, depth, agentIndex, gameState):
        if (gameState.isWin() or gameState.isLose() or depth >= self.depth):
            return self.evaluationFunction(gameState), None
        
        scores = []
        isMinplayer = True if agentIndex != 0 else False
        bestScore = float("inf") if isMinplayer else float("-inf")
        legalMoves = gameState.getLegalActions(agentIndex)
        nextIndex = (agentIndex + 1) % gameState.getNumAgents() # 0 -> 1 -> 2 -> 0 -> 1 -> 2 -> ...
        
        if nextIndex == 0:
            depth +=1

        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        for move in legalMoves:
            nextState = gameState.getNextState(agentIndex, move)
            nextValue, __ = self.performExpectimax(depth, nextIndex, nextState)
            bestScore = min(bestScore, nextValue) if isMinplayer else max(bestScore, nextValue)
            scores.append(nextValue)
        
        if isMinplayer:
            s = sum(scores)
            l = len(scores)
            return s/l, None
        else:
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            choisenIndex = random.choice(bestIndices)
            return max(scores), legalMoves[choisenIndex]
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")

    # pacman_position = currentGameState.getPacmanPosition()
    # ghost_positions = currentGameState.getGhostPositions()

    # food_list = currentGameState.getFood().asList()
    # food_count = len(food_list)
    # capsule_count = len(currentGameState.getCapsules())
    # closest_food = 1

    # game_score = currentGameState.getScore()

    # # Find distances from pacman to all food
    # food_distances = [manhattanDistance(pacman_position, food_position) for food_position in food_list]

    # # Set value for closest food if there is still food left
    # if food_count > 0:
    #     closest_food = min(food_distances)

    # # Find distances from pacman to ghost(s)
    # for ghost_position in ghost_positions:
    #     ghost_distance = manhattanDistance(pacman_position, ghost_position)

    #     # If ghost is too close to pacman, prioritize escaping instead of eating the closest food
    #     # by resetting the value for closest distance to food
    #     if ghost_distance < 2:
    #         closest_food = 99999

    # features = [1.0 / closest_food,
    #             game_score,
    #             food_count,
    #             capsule_count]

    # weights = [10,
    #            200,
    #            -10,
    #            -100]

    # Linear combination of features
    # return sum([feature * weight for feature, weight in zip(features, weights)])

    pacmanPos = currentGameState.getPacmanPosition()
    ghostsState = [(manhattanDistance(pacmanPos, currentGameState.getGhostPosition(Id)), Id) for Id in range(1, currentGameState.getNumAgents())]
    minGhostDist, minGhostId = (0, 0) if len(ghostsState) == 0 else min(ghostsState)
    ghostsDist = [x for x, y in ghostsState]

    # print(minGhostDist)
    isEat = currentGameState.data.agentStates[minGhostId].scaredTimer > 1
    curScore = currentGameState.getScore()
    
    # food
    foodDist = [manhattanDistance(pacmanPos, food) for food in currentGameState.getFood().asList()]
    numFood = currentGameState.getNumFood()
    minFoodDist = 1 if numFood == 0 else min(foodDist)
    avgFoodDist = 1 if numFood == 0 else sum(foodDist) / len(foodDist)

    # capsules
    numCapsules = len(currentGameState.getCapsules())
    capsulesDist = [manhattanDistance(pacmanPos, capsule) for capsule in currentGameState.getCapsules()]
    minCapsuleDist = 0 if len(currentGameState.getCapsules()) == 0 else min( capsulesDist )

    if isEat:
        return 100 * curScore + (-30 * minGhostDist)
    
    if minCapsuleDist < 6 :
        return 100 * curScore + (-50 * numCapsules )  + (-30 * minCapsuleDist) + (-20 * minGhostDist)
    
    if numCapsules == 0:
        return 100 * curScore + (-30 * minFoodDist) + (-30* numFood) + (30 * minGhostDist)
    return 80 * curScore + (-30 * minFoodDist) + (-30 * numFood) + (-20 * minCapsuleDist)  + (-20 * numCapsules)  + (-10 * minGhostDist)
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
