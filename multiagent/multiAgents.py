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

        comida = newFood.asList()
        distMinimaComida = 99999999
        for c in comida:
            distancia = util.manhattanDistance(newPos, c)
            if distancia < distMinimaComida:
                distMinimaComida = distancia

        distMinimaFantasma = 99999999
        for c in newGhostStates:
            distancia = util.manhattanDistance(newPos, c.getPosition())
            if distancia <= 1:
               return -99999999     
            if distancia < distMinimaFantasma:
                distMinimaFantasma = distancia
        
        return successorGameState.getScore() + 1/(float(distMinimaComida)+1)  - 1/(float(distMinimaFantasma)+1) 

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


        def ret_2nd_ele(tuple_1):
            return tuple_1[1]

        def minimax(agente, profundidade, gameState):
            listaEstados = []
            if gameState.isLose() or gameState.isWin() or profundidade == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return "stop" , self.evaluationFunction(gameState)

            if agente == 0:  
                for estado in gameState.getLegalActions(agente):
                    _ , custo = minimax(1, profundidade , gameState.generateSuccessor(agente, estado))
                    proximoEstado = (estado, custo)
                    listaEstados.append(proximoEstado)
                return max(listaEstados ,key=ret_2nd_ele)


            else:  
                proximoAgente = agente + 1  
                if gameState.getNumAgents() == proximoAgente:
                    proximoAgente = 0
                if proximoAgente == 0:
                    profundidade += 1
                for estado in gameState.getLegalActions(agente):
                    _ , custo = minimax(proximoAgente, profundidade , gameState.generateSuccessor(agente, estado))
                    proximoEstado = (estado , custo)
                    listaEstados.append(proximoEstado)
                return min(listaEstados, key=ret_2nd_ele)   
                

        agentePac = 0
        acao, valor = minimax(agentePac, 0, gameState)
        return acao

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def alphabeta(agente, profundidade, gameState, a, b):
            
            if gameState.isLose() or gameState.isWin() or profundidade == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return "stop" , self.evaluationFunction(gameState)

            if agente == 0:  
                v = float("-inf")
                for estado in gameState.getLegalActions(agente):
                    _ , custo = alphabeta(1, profundidade , gameState.generateSuccessor(agente, estado),a,b)
                    if custo > v:
                        v = custo
                        melhorEstado = estado
                    if v > b:
                        return estado , v
                    a = max(a, v)
                return melhorEstado, v

            else:    
                proximoAgente = agente + 1  
                if gameState.getNumAgents() == proximoAgente:
                    proximoAgente = 0
                if proximoAgente == 0:
                    profundidade += 1

                v = float("inf")   
                for estado in gameState.getLegalActions(agente):
                    _ , custo = alphabeta(proximoAgente, profundidade , gameState.generateSuccessor(agente, estado), a , b)
                    if custo < v:
                        v = custo
                        melhorEstado = estado
                    if v < a:
                        return estado , v
                    b = min(b, v)
                return melhorEstado, v        
                

        agentePac = 0
        alpha = float("-inf")
        beta = float("inf")
        acao, valor = alphabeta(agentePac, 0, gameState, alpha, beta)
        return acao
        
        util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        def ret_2nd_ele(tuple_1):
            return tuple_1[1]

        def expectimax(agente, profundidade, gameState):
            listaEstados = []
            if gameState.isLose() or gameState.isWin() or profundidade == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return "stop" , self.evaluationFunction(gameState)

            if agente == 0:  
                for estado in gameState.getLegalActions(agente):
                    _ , custo = expectimax(1, profundidade , gameState.generateSuccessor(agente, estado))
                    proximoEstado = (estado, custo)
                    listaEstados.append(proximoEstado)
                return max(listaEstados ,key=ret_2nd_ele)


            else:  
                proximoAgente = agente + 1  
                if gameState.getNumAgents() == proximoAgente:
                    proximoAgente = 0
                if proximoAgente == 0:
                    profundidade += 1

                custototal = 0 
                for estado in gameState.getLegalActions(agente):
                    _ , custo = expectimax(proximoAgente, profundidade , gameState.generateSuccessor(agente, estado))
                    custototal += custo
                return "stop", custototal / len(gameState.getLegalActions(agente))
                

        agentePac = 0
        acao, valor = expectimax(agentePac, 0, gameState)
        return acao
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    """
    "*** YOUR CODE HERE ***"
    posicaoPac = currentGameState.getPacmanPosition()
    aux = currentGameState.getFood()
    comida = aux.asList()

    "*** YOUR CODE HERE ***"

    distMinimaComida = 99999999
    for c in comida:
        distancia = util.manhattanDistance(posicaoPac, c)
        if distancia < distMinimaComida:
            distMinimaComida = distancia

    distMinimaFantasma = 99999999
    for c in currentGameState.getGhostStates():
        distancia = util.manhattanDistance(posicaoPac, c.getPosition())
        if distancia <= 1:
           return -99999999     
        if distancia < distMinimaFantasma:
            distMinimaFantasma = distancia   

    bolao = currentGameState.getCapsules()
    boloes = len(bolao)
    
    return 100 * currentGameState.getScore() + 1/(float(distMinimaComida)+1)  - 1/(float(distMinimaFantasma)+1) - boloes
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
