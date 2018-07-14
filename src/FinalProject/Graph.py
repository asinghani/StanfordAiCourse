import numpy as np
from graphviz import Digraph
from Queue import Queue, PriorityQueue

class Node:
    index = 0
    arbitraryIndex = 0
    def __init__(self, data=None):
        self.data = data

        if data is None:
            self.data = Node.index
            self.defaultName = True
            Node.index = Node.index + 1
        else:
            self.defaultName = False

        self.index = Node.arbitraryIndex
        Node.arbitraryIndex = Node.arbitraryIndex + 1

    def getData(self):
        return self.data

    def __repr__(self):
        return "Node(data="+str(self.data)+")"

class Graph:
    def getNumNodes(self):
        raise NotImplementedError()

    def getAllNodes(self):
        raise NotImplementedError()

    def getAccessibleNodes(self, node):
        raise NotImplementedError()

    def getAccessibleNodesWithCost(self, node):
        raise NotImplementedError()

    def getCost(self, node1, node2):
        raise NotImplementedError()

    def aStarHeuristic(self, node1, node2):
        return 0 # Turns A* into Dijkstra's algorithm

    def visualizeGraph(self):
        f = Digraph("graph", filename="graph.gv")
        f.attr(rankdir="LR", size="8,5")
        f.node_attr.update(color='lightblue2', style='filled')

        for node in self.getAllNodes():
            nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
            f.node(nodeName)

            for node2, cost in self.getAccessibleNodesWithCost(node):
                node2Name = str(node2.data) if not node2.defaultName else "Node {}".format(node2.data)

                if self.getCost(node2, node) == self.getCost(node, node2):
                    if node.index < node2.index:
                        f.attr("edge", arrowhead="none")
                        f.edge(nodeName, node2Name, "Cost = {}".format(cost))
                        f.attr("edge", arrowhead="normal")
                else:
                    f.edge(nodeName, node2Name, "Cost = {}".format(cost))

        print("Rendered to " + f.render())

    def visualizeGraphWithPath(self, path):
        f = Digraph("graph", filename="graph.gv")
        f.attr(rankdir="LR", size="8,5")
        f.node_attr.update(color='lightblue2', style='filled')

        for node in self.getAllNodes():
            nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
            f.node(nodeName)

            for node2, cost in self.getAccessibleNodesWithCost(node):
                node2Name = str(node2.data) if not node2.defaultName else "Node {}".format(node2.data)

                if self.getCost(node2, node) == self.getCost(node, node2):
                    if node.index < node2.index:
                        f.attr("edge", arrowhead="none")
                        f.edge(nodeName, node2Name, "Cost = {}".format(cost))
                        f.attr("edge", arrowhead="normal")
                else:
                    f.edge(nodeName, node2Name, "Cost = {}".format(cost))

        f.attr("edge", color="red")
        for i in range(len(path) - 1):
            node = path[i]
            node2 = path[i + 1]
            nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
            node2Name = str(node2.data) if not node2.defaultName else "Node {}".format(node2.data)
            f.edge(nodeName, node2Name, "{}".format(i + 1))

        print("Rendered to " + f.render())

    def aStar(self, startNode, endNode):
        frontier = PriorityQueue()
        frontier.put((0, startNode))
        prev = {}
        cumulativeCost = {}
        prev[startNode] = None
        cumulativeCost[startNode] = 0

        while not frontier.empty():
            priority, current = frontier.get()

            if current == endNode:
                break

            for node, cost in self.getAccessibleNodesWithCost(current):
                newCost = cumulativeCost[current] + cost
                if node not in cumulativeCost or newCost < cumulativeCost[node]:
                    cumulativeCost[node] = newCost
                    frontier.put((newCost + self.aStarHeuristic(node, endNode), node))
                    prev[node] = current


        path = [endNode]

        while path[-1] != startNode:
            path.append(prev[path[-1]])

        return path[::-1]


    def multiBfs(self, startNode, endNode):
        currentLevel = Queue()
        visited = set([])


        paths = []

        currentLevel.put([startNode])

        while not currentLevel.empty():
            currentPath = currentLevel.get()
            baseNode = currentPath[-1]

            for nextNode in self.getAccessibleNodes(baseNode):
                if nextNode in currentPath:
                    continue
                newPath = currentPath + [nextNode]

                if nextNode == endNode:
                    paths.append(newPath)
                else:
                    currentLevel.put(newPath)

        return paths



    def bfs(self, startNode, endNode):

        def convertAllToLists(node, prevDict):
            if node == startNode:
                return [[startNode]]

            outerList = []
            for prevNode in prevDict[node]:
                l = convertAllToLists(prevNode, prevDict)
                l = [path + [node] for path in l]
                outerList = outerList + l

            return outerList


        currentLevel = Queue()
        visited = set([])

        prev = {}

        prev[startNode] = None
        currentLevel.put(startNode)

        #visited.add(startNode)
        while not currentLevel.empty():
            baseNode = currentLevel.get()
            print(baseNode)

            for nextNode in self.getAccessibleNodes(baseNode):
                if nextNode in prev[baseNode]:
                    continue

                if True: # nextNode not in currentLevel.queue:
                    if nextNode not in prev:
                        prev[nextNode] = []

                    prev[nextNode].append(baseNode)

                    #if nextNode not in currentLevel.queue:
                    currentLevel.put(nextNode)

            visited.add(baseNode)

        return [l for l in convertAllToLists(endNode, prev)]


    def dfs(self, startNode, endNode):
        currPoint = startNode
        unvisitedQueue = PriorityQueue()
        visited = []
        path = []

        while currPoint != endNode:
            visited.append(currPoint)
            path.append(currPoint)

            availableNodes = self.getAccessibleNodes(currPoint)

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

    def dijsktraTree(self, startNode, earlyStop=None):
        frontier = PriorityQueue()
        frontier.put((0, startNode))
        prev = {}
        cumulativeCost = {}
        prev[startNode] = None
        cumulativeCost[startNode] = 0

        while not frontier.empty():
            priority, current = frontier.get()

            if current == earlyStop:
                break

            for node, cost in self.getAccessibleNodesWithCost(current):
                newCost = cumulativeCost[current] + cost
                if node not in cumulativeCost or newCost < cumulativeCost[node]:
                    cumulativeCost[node] = newCost
                    frontier.put((newCost, node))
                    prev[node] = current

        return prev

    def dijsktraSearch(self, startNode, endNode):
        tree = self.dijsktraTree(startNode, earlyStop = endNode)
        path = [endNode]

        while path[-1] != startNode:
            path.append(tree[path[-1]])

        return path[::-1]

