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

def depthFirstSearch(problem: SearchProblem):
    """
    comando uteis
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    #a stack garante que o proximo nodo a ser visto sera um dos filhos do ultimo nodo analizado
    fronteira = util.Stack()
    #nodos ja explorados
    jaExplorados = []

    #o nodo eh a formado por um estado do tabuleiro e a lista de acoes
    inicio = (problem.getStartState(), [])

    #coloca o nodo inicio 
    fronteira.push(inicio)
    

    while not fronteira.isEmpty():
        #remove o ultimo elemento colocado
        estado, caminho = fronteira.pop()

        # se o estado for o final pare
        if problem.isGoalState(estado):
                return caminho
        
        #evita repeticao de nodos 
        if estado not in jaExplorados:
            #colocar o nodo atual no jaExplorados
            jaExplorados.append(estado)
            #pega a lista de estados sucessores 
            sucessores = problem.getSuccessors(estado)
            #coloca os sucessores na fronteira
            for novoEstado, proxAcao , lixo in sucessores:
                novoAcao = caminho + [proxAcao]
                novoNodo = (novoEstado, novoAcao)
                fronteira.push(novoNodo)

    return caminho  
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    #a queue garante que o proximo nodo a ser visto sera o que foi colocado a mais tempo
    fronteira = util.Queue()
    #nodos ja explorados
    jaExplorados = []

    #o nodo eh a formado por um estado do tabuleiro e a lista de acoes
    inicio = (problem.getStartState(), [])

    #coloca o nodo inicio 
    fronteira.push(inicio)
    
    while not fronteira.isEmpty():
        #remove o ultimo elemento colocado
        estado, caminho = fronteira.pop()
        # se o estado for o final pare
        if problem.isGoalState(estado):
                return caminho

        #evita repeticao de nodos 
        if estado not in jaExplorados:
            #colocar o nodo atual no jaExplorados
            jaExplorados.append(estado)
            #pega a lista de estados sucessores 
            sucessores = problem.getSuccessors(estado)
            for novoEstado, proxAcao , lixo in sucessores:
                novoAcao = caminho + [proxAcao]
                novoNodo = (novoEstado, novoAcao)
                fronteira.push(novoNodo)

    return caminho 
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
	#a queue garante que o proximo nodo a ser visto sera o com menor custo
	fronteira = util.PriorityQueue()
	#nodos ja explorados
	jaExplorados = []

	#o nodo eh a formado por um estado do tabuleiro e a lista de acoes
	inicio = (problem.getStartState(), [], 0)

	#coloca o nodo inicio 
	#agora contem o custo dos antecessores
	fronteira.push(inicio,0)

	while not fronteira.isEmpty():
		#remove o ultimo elemento colocado
		estado, caminho,custoPai = fronteira.pop()
		# se o estado for o final pare
		if problem.isGoalState(estado):
			return caminho

		#evita repeticao de nodos 
		if estado not in jaExplorados:
			#colocar o nodo atual no jaExplorados
			jaExplorados.append(estado)
			#pega a lista de estados sucessores 
			sucessores = problem.getSuccessors(estado)
			#coloca os sucessores na fronteira
			for novoEstado, proxAcao , custo in sucessores:
				novoCusto = custo + custoPai
				novoAcao = caminho + [proxAcao]
				novoNodo = (novoEstado, novoAcao, novoCusto)
				fronteira.push(novoNodo,novoCusto)

	return caminho 
	util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
	#a queue garante que o proximo nodo a ser visto sera o com menor custo
	fronteira = util.PriorityQueue()

	#nodos ja explorados
	jaExplorados = [] 

	#o nodo eh a formado por um estado do tabuleiro e a lista de acoes
	inicio = (problem.getStartState(), [], 0)

	#coloca o nodo inicio 
    #agora contem o custo dos antecessores
	fronteira.push(inicio,heuristic(problem.getStartState(),problem))
    
	while not fronteira.isEmpty():
		#remove o ultimo elemento colocado
		estado, caminho, custoPai = fronteira.pop()
		# se o estado for o final pare
		if problem.isGoalState(estado):
			return caminho

		#evita repeticao de nodos 
		if estado not in jaExplorados:
			#colocar o nodo atual no jaExplorados
			jaExplorados.append(estado)
			#pega a lista de estados sucessores 
			sucessores = problem.getSuccessors(estado)
			#coloca os sucessores na fronteira
			for novoEstado, proxAcao , custo in sucessores:
				novoCusto = custo + custoPai
				novoAcao = caminho + [proxAcao]
				novoNodo = (novoEstado, novoAcao, novoCusto)
				fronteira.push(novoNodo,novoCusto + heuristic(novoEstado,problem))
			
	return caminho
	util.raiseNotDefined()
	

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
