import numpy as np
from graphviz import Digraph
from Queue import Queue, PriorityQueue

class AdjacencyMatrixGraph:
    def __init__(self, width, height, adjacencyMatrix=None):
        self.numNodes = numNodes
        self.Grid = np.zeros((width, height))
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
                    if self.adjacencyMatrix[j][i] == self.adjacencyMatrix[i][j]:
                        if i < j:
                            f.attr("edge", arrowhead="none")
                            f.edge("Node {}".format(i), "Node {}".format(j), "Cost = {}".format(self.adjacencyMatrix[i][j]))
                            f.attr("edge", arrowhead="normal")
                    else:
                        f.edge("Node {}".format(i), "Node {}".format(j), "Cost = {}".format(self.adjacencyMatrix[i][j]))

        f.attr("edge", color="red")
        for i in range(len(path) - 1):
            f.edge("Node {}".format(path[i]), "Node {}".format(path[i+1]), "{}".format(i + 1))
        print("Rendered to " + f.render())

    def bfs(self, startNode, endNode):

        def convertToList(prevDict):
            l = [endNode]
            while l[-1] != startNode:
                l.append(prevDict[l[-1]])

            return l[::-1]

        currentLevel = Queue()
        visited = set([])

        prev = {}

        prev[startNode] = None
        currentLevel.put(startNode)

        while not currentLevel.empty():
            baseNode = currentLevel.get()
            if baseNode == endNode:
                return convertToList(prev)

            for nextNode in self.getAccessibleNodes(baseNode)[0]:
                if nextNode in visited:
                    continue

                if nextNode not in currentLevel.queue:
                    prev[nextNode] = baseNode

                    currentLevel.put(nextNode)

            visited.add(baseNode)

    def dfs(self, startNode, endNode):
        currPoint = startNode
        unvisitedQueue = PriorityQueue()
        visited = []
        path = []

        while currPoint != endNode:
            visited.append(currPoint)
            path.append(currPoint)

            availableNodes = self.getAccessibleNodes(currPoint)[0].tolist()

            for visitedNode in visited:
                if visitedNode in availableNodes:
                    availableNodes.remove(visitedNode)

            if availableNodes.__len__() == 0:
                nextNode = unvisitedQueue.get(False)
                if nextNode == None:
                    print("Failed")
                    return None

                path = path[:path.index(nextNode[1][0])+1]
                nextNode = nextNode[1][1]

            elif availableNodes.__len__() == 1:
                nextNode = availableNodes[0]

            else:
                nextNode = availableNodes[0]
                availableNodes = availableNodes[1:]
                x = 0
                for i in availableNodes:
                    x = x + 1
                    unvisitedQueue.put((-1 * (path.__len__() + x), [currPoint, i]))

            currPoint = nextNode

        path.append(endNode)

        return path

    def dijktra(self, startNode, endNode):
        pass
