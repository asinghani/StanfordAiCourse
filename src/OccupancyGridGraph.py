import numpy as np
from graphviz import Digraph
from Queue import Queue, PriorityQueue
from Graph import Graph, Node

class OccupancyGridGraph(Graph):
    def __init__(self, width, height, occupancyGrid=None):
        self.width = width
        self.height = height
        self.numNodes = width * height
        self.occupancyGrid = occupancyGrid

        if self.occupancyGrid is None:
            self.occupancyGrid = np.zeros((height, width))
            self.nodes = [[Node(data=str((y, x))) for x in range(width)] for y in range(height)]

    def getNumNodes(self):
        return self.numNodes

    def getAllNodes(self):
        return sum(self.nodes, [])

    def setObstacle(self, x, y, obstacle = 1):
        self.occupancyGrid[y][x] = obstacle

    def _parseTuple(self, tupleStr):
        x, y = tupleStr.replace("(", "").replace(")", "").replace(" ", "").split(",")
        x = int(x)
        y = int(y)
        return (x, y)

    def getAccessibleNodes(self, node):
        x, y = self._parseTuple(node.data)
        availList = []

        if self.occupancyGrid[x][y] == 1:
            return []

        if x + 1 < self.occupancyGrid.shape[0] and self.occupancyGrid[x + 1][y] == 0:
            availList.append(self.nodes[x + 1][y])

        if x - 1 >= 0 and self.occupancyGrid[x - 1][y] == 0:
            availList.append(self.nodes[x - 1][y])

        if y + 1 < self.occupancyGrid.shape[1] and self.occupancyGrid[x][y + 1] == 0:
            availList.append(self.nodes[x][y + 1])

        if y - 1 >= 0 and self.occupancyGrid[x][y - 1] == 0:
            availList.append(self.nodes[x][y - 1])

        return availList

    def getAccessibleNodesWithCost(self, node):
        availList = self.getAccessibleNodes(node)
        return [(node, 1.0) for node in availList]

    def getCost(self, node1, node2):
        if node2 in self.getAccessibleNodes(node1):
            return 1.0
        else:
            return 0

    def printGraph(self):
        for i in range(self.height):
            str = ""
            for j in range(self.width):
                str = str + ("." if self.occupancyGrid[i][j] == 0 else "#")

            print(str)

        print("")
