actions = [0, 3, 5, 4, 0, 2, 0, 3, 5, 1]

from AdjacencyMatrixGraph import AdjacencyMatrixGraph as Graph
g = Graph(6)
g.addEdge(0, 3, directed=True, cost=5)
g.addEdge(3, 5, directed=True, cost=5)
g.addEdge(5, 1, directed=True, cost=3)
g.addEdge(0, 2, directed=False, cost=8)
g.addEdge(4, 5, directed=False, cost=8)
g.addEdge(4, 0, directed=True, cost=958)
g.visualizeGraphWithPath(actions)
