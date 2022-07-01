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
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    """Search the deepest nodes in the search tree first."""

    #a stack garante que o proximo nodo a ser visto sera um dos filhos do ultimo nodo analizado
    fronteira = util.Stack()
    #nodos ja explorados
    jaExplorados = []

    #o nodo eh a formado por um estado do tabuleiro e a lista de acoes
    # que vao do estado inicial ate o final (que sera chamada de daminho)
    inicio = (problem.getStartState(), [])
    
    fronteira.push((problem.getStartState(),[]))
    
    while not fronteira.isEmpty():
        #begin exploring last (most-recently-pushed) node on frontier
        estado, caminho = fronteira.pop()

        if problem.isGoalState(estado):
                return caminho
        
        if estado not in jaExplorados:
            #mark current node as explored
            jaExplorados.append(estado)
            #get list of possible successor nodes in 
            #form (successor, action, stepCost)
            sucessores = problem.getSuccessors(estado)
            #push each successor to frontier ''''
            for novoEstado, proxAcao , lixo in sucessores:
                novoAcao = caminho + [proxAcao]
                novoNodo = (novoEstado, novoAcao)
                fronteira.push(novoNodo)

    return caminho  

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #a stack garante que o proximo nodo a ser visto sera um dos filhos do ultimo nodo analizado
    fronteira = util.Queue()
    #nodos ja explorados
    jaExplorados = []

    #o nodo eh a formado por um estado do tabuleiro e a lista de acoes
    # que vao do estado inicial ate o final (que sera chamada de daminho)
    inicio = (problem.getStartState(), [])
    
    fronteira.push(inicio)
    
    while not fronteira.isEmpty():
        #begin exploring last (most-recently-pushed) node on frontier
        estado, caminho = fronteira.pop()

        if problem.isGoalState(estado):
                return caminho
        
        if estado not in jaExplorados:
            #mark current node as explored
            jaExplorados.append(estado)
            #get list of possible successor nodes in 
            #form (successor, action, stepCost)
            sucessores = problem.getSuccessors(estado)
            #push each successor to frontier ''''
            for novoEstado, proxAcao , lixo in sucessores:
                novoAcao = caminho + [proxAcao]
                novoNodo = (novoEstado, novoAcao)
                fronteira.push(novoNodo)

    return caminho 
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fronteira = util.PriorityQueue()
    #nodos ja explorados
    jaExplorados = []

    #o nodo eh a formado por um estado do tabuleiro e a lista de acoes
    # que vao do estado inicial ate o final (que sera chamada de daminho)
    inicio = (problem.getStartState(), [], 0)
    
    fronteira.push(inicio,0)
    
    while not fronteira.isEmpty():
        #begin exploring last (most-recently-pushed) node on frontier
        estado, caminho,custoPai = fronteira.pop()
        
        if problem.isGoalState(estado):
            return caminho

        if estado not in jaExplorados:
            #mark current node as explored
            jaExplorados.append(estado)
            #get list of possible successor nodes in 
            #form (successor, action, stepCost)
            sucessores = problem.getSuccessors(estado)
            #push each successor to frontier ''''
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
	"""Search the node that has the lowest combined cost and heuristic first."""

	"*** YOUR CODE HERE ***"

	fronteira = util.PriorityQueue()
	#nodos ja explorados
	jaExplorados = [] 

	#o nodo eh a formado por um estado do tabuleiro e a lista de acoes
	# que vao do estado inicial ate o final (que sera chamada de daminho)
	inicio = (problem.getStartState(), [], 0)

	fronteira.push(inicio,heuristic(problem.getStartState(),problem))

	while not fronteira.isEmpty():
		#begin exploring last (most-recently-pushed) node on frontier

		estado, caminho,h = fronteira.pop()

		if problem.isGoalState(estado):
			#print(caminho)
			return caminho

		flag = 1
		for aux in jaExplorados:
			(e,a,c) = aux
			if (e == estado):
				flag = 0
		if (flag == 1): 		
			#if estado not in jaExplorados:	
			#mark current node as explored
			jaExplorados.append((estado,caminho,h))
			#get list of possible successor nodes in 
			#form (successor, action, stepCost)
			sucessores = problem.getSuccessors(estado)
			#push each successor to frontier 
			for novoEstado, proxAcao , custo in sucessores:
				novoAcao = caminho + [proxAcao]
				novoCusto = problem.getCostOfActions(novoAcao)
				#novoCusto = custoPai + custo 
				#if (novoEstado,_,_) is in fronteira:
				flag = 0
				for aux in jaExplorados:
					(e,a,c) = aux
					if (e == novoEstado):
						flag = 1
						if (novoCusto < problem.getCostOfActions(a)):
							novoNodo = (novoEstado, novoAcao, novoCusto)
							fronteira.update(novoNodo,novoCusto + heuristic(novoEstado,problem))
						break
				if flag == 0:
					novoNodo = (novoEstado, novoAcao, novoCusto )
					fronteira.push(novoNodo,novoCusto + heuristic(novoEstado,problem))	
					#jaExplorados.append((novoEstado, novoAcao, novoCusto))

	#print(caminho)				
	return caminho
	util.raiseNotDefined()

	'''

	fronteira = util.PriorityQueue()
	#nodos ja explorados
	jaExplorados = [] 

	#o nodo eh a formado por um estado do tabuleiro e a lista de acoes
	# que vao do estado inicial ate o final (que sera chamada de daminho)
	inicio = (problem.getStartState(), [], 0)

	fronteira.push(inicio,0)

	while not fronteira.isEmpty():
		#begin exploring last (most-recently-pushed) node on frontier

		estado, caminho,custoPai = fronteira.pop()

		if problem.isGoalState(estado):
			return caminho

		if estado not in jaExplorados:	
			#mark current node as explored
			jaExplorados.append((estado,caminho,custoPai))
			#get list of possible successor nodes in 
			#form (successor, action, stepCost)
			sucessores = problem.getSuccessors(estado)
			#push each successor to frontier 
			for novoEstado, proxAcao , custo in sucessores:
				novoAcao = caminho + [proxAcao]
				novoCusto = problem.getCostOfActions(novoAcao)
				#novoCusto = custoPai + custo 
				#if (novoEstado,_,_) is in fronteira:
				flag = 0
				for (e,a,c) in jaExplorados:
					if e == novoEstado and novoCusto >= c : 
						#novoNodo = (novoEstado, novoAcao, novoCusto + heuristic(novoEstado,problem))
						#fronteira.update(novoNodo,novoCusto)
						flag = 1
						break
				if flag == 0:
					novoNodo = (novoEstado, novoAcao, novoCusto )
					fronteira.push(novoNodo,novoCusto + heuristic(novoEstado,problem))	
					#jaExplorados.append((novoEstado, novoAcao, novoCusto))

	
	util.raiseNotDefined()
	'''
	'''
	for each neighbor of current
	tentative_gScore := gScore[current] + d(current, neighbor)
	if tentative_gScore < gScore[neighbor]
	    cameFrom[neighbor] := current
	    gScore[neighbor] := tentative_gScore
	    fScore[neighbor] := tentative_gScore + h(neighbor)
	    if neighbor not in openSet
	        openSet.add(neighbor)
	'''	

	#return caminho
	


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
