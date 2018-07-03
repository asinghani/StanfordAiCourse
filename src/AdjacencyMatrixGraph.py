import numpy as np
from graphviz import Digraph
from Queue import Queue

class AdjacencyMatrixGraph:
    def __init__(self, numNodes, adjacencyMatrix=None):
        self.numNodes = numNodes
        self.adjacencyMatrix = np.zeros((numNodes, numNodes))
        if adjacencyMatrix is not None:
            for i in range(numNodes):
                for j in range(numNodes):
                    self.adjacencyMatrix[i][j] = adjacencyMatrix[i][j]

    def addEdge(self, node1, node2, cost=1, directed=False):
        self.adjacencyMatrix[node1][node2] = cost
        if not directed:
            self.adjacencyMatrix[node2][node1] = cost

    def getAccessibleNodes(self, node):
        return np.nonzero(self.adjacencyMatrix[node])

    def getAccessibleNodesWithCost(self, node):
        nodes = np.nonzero(self.adjacencyMatrix[node])
        nodes = [(n, self.adjacencyMatrix[node][n]) for n in nodes]
        return nodes

    def visualizeGraph(self):
        f = Digraph("graph", filename="graph.gv")
        f.attr(rankdir="LR", size="8,5")
        f.node_attr.update(color='lightblue2', style='filled')

        for i in range(self.numNodes):
            f.node("Node {}".format(i))
            for j in range(self.numNodes):
                if self.adjacencyMatrix[i][j] != 0:
                    f.edge("Node {}".format(i), "Node {}".format(j), "Cost = {}".format(self.adjacencyMatrix[i][j]))

        print("Rendered to " + f.render())

    def visualizeGraphWithPath(self, path):
        f = Digraph("graph", filename="graph.gv")
        f.attr(rankdir="LR", size="8,5")
        f.attr("edge", color="black")
        f.node_attr.update(color='lightblue2', style='filled')
        for i in range(self.numNodes):
            f.node("Node {}".format(i))
            for j in range(self.numNodes):
                if self.adjacencyMatrix[i][j] != 0:
                    f.edge("Node {}".format(i), "Node {}".format(j), "Cost = {}".format(self.adjacencyMatrix[i][j]))

        f.attr("edge", color="red")
        for i in range(len(path) - 1):
            f.edge("Node {}".format(path[i]), "Node {}".format(path[i+1]), "{}".format(i + 1))
        print("Rendered to " + f.render())

    def bfs(self, startEdge, endNode):
        currentLevel = Queue()
        visited = set([])
