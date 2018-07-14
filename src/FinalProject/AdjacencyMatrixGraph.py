import numpy as np
from graphviz import Digraph
from Queue import Queue, PriorityQueue
from Graph import Graph, Node

class AdjacencyMatrixGraph(Graph):
    def __init__(self, numNodes, adjacencyMatrix=None):
        self.numNodes = numNodes
        self.nodes = [Node(data=i) for i in range(numNodes)]
        self.adjacencyMatrix = np.zeros((numNodes, numNodes))
        if adjacencyMatrix is not None:
            for i in range(numNodes):
                for j in range(numNodes):
                    self.adjacencyMatrix[i][j] = adjacencyMatrix[i][j]


    def getNumNodes(self):
        return self.numNodes

    def getAllNodes(self):
        return self.nodes

    def getAccessibleNodes(self, node):
        nodeIndex = self.nodes.index(node)
        nodes = np.nonzero(self.adjacencyMatrix[nodeIndex])
        return [self.nodes[n] for n in nodes[0]]

    def getAccessibleNodesWithCost(self, node):
        nodeIndex = self.nodes.index(node)
        nodes = np.nonzero(self.adjacencyMatrix[nodeIndex])
        return [(self.nodes[n], self.adjacencyMatrix[nodeIndex][n]) for n in nodes[0]]

    def getCost(self, node1, node2):
        node1Index = self.nodes.index(node1)
        node2Index = self.nodes.index(node2)
        return self.adjacencyMatrix[node1Index][node2Index]

    def addEdge(self, node1, node2, cost=1, directed=False):
        if isinstance(node1, Node):
            _node1 = self.nodes.index(node1)
        else:
            _node1 = node1

        if isinstance(node2, Node):
            _node2 = self.nodes.index(node2)
        else:
            _node2 = node2

        self.adjacencyMatrix[_node1][_node2] = cost
        if not directed:
            self.adjacencyMatrix[_node2][_node1] = cost
