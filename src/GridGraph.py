from AdjacencyMatrixGraph import AdjacencyMatrixGraph
from graphviz import Digraph
from Graph import Node
from functools import partial

def parsePosToGvizCoords(string):
    string = string.replace("(", "").replace(")", "").replace(" ", "")
    x, y = string.split(",")
    return "{},{}!".format(int(y) * 3, int(x) * -3)

def visualizeGraph(self, showCost=True):
    f = Digraph("graph", filename="graph.gv", engine='neato')
    f.attr(rankdir="RL", size="8,5")
    f.node_attr.update(color='lightblue2', style='filled')

    # Draw Nodes
    for node in self.getAllNodes():
        nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
        f.attr("node", pos=parsePosToGvizCoords(node.data))
        f.node(nodeName)

    # Draw Edges
    for node in self.getAllNodes():
        nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
        for node2, cost in self.getAccessibleNodesWithCost(node):
            node2Name = str(node2.data) if not node2.defaultName else "Node {}".format(node2.data)

            if self.getCost(node2, node) == self.getCost(node, node2):
                if node.index < node2.index:
                    f.attr("edge", arrowhead="none")
                    f.edge(nodeName, node2Name, "Cost = {}".format(cost) if showCost else None)
                    f.attr("edge", arrowhead="normal")
            else:
                f.edge(nodeName, node2Name, "Cost = {}".format(cost) if showCost else None)

    print("Rendered to " + f.render())

"""def _________visualizeGraphWithPath(self, path):
    f = Digraph("graph", filename="graph.gv", engine='neato')
    f.attr(rankdir="LR", size="8,5")

    f.node_attr.update(color='lightblue2', style='filled')
    for i in range(4):
        for j in range(3):
            if (i,j) in [(1,3), (2, 2), (1,1)]:
                continue
            f.attr("node", pos="{},{}!".format(i*3, j*3))
            f.node("({}, {})".format(i, j))

    f.edge("(0, 0)","(1, 0)", "Cost = {}".format(503.3))

    print("Rendered to " + f.render())
"""

def visualizeGraphWithPath(self, path, showCost=True, currentPos=None, currentEdge=None):
    f = Digraph("graph", filename="graph", format="png", engine='neato')
    f.attr(rankdir="RL", size="16, 10")
    f.node_attr.update(color='lightblue2', style='filled')

    # Draw Nodes
    for node in self.getAllNodes():
        if currentPos is not None and str(currentPos) == node.data:
            f.attr("node", color="green")
        else:
            f.attr("node", color="lightblue2")

        nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
        f.attr("node", pos=parsePosToGvizCoords(node.data))
        f.node(nodeName)

    # Draw Edges
    for node in self.getAllNodes():
        nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
        for node2, cost in self.getAccessibleNodesWithCost(node):
            node2Name = str(node2.data) if not node2.defaultName else "Node {}".format(node2.data)

            if currentEdge is not None and ((str(currentEdge[0]) == node.data and str(currentEdge[1]) == node2.data) or (str(currentEdge[0]) == node2.data and str(currentEdge[1]) == node.data)):
                f.attr("edge", color="green")
            else:
                f.attr("edge", color="black")

            if self.getCost(node2, node) == self.getCost(node, node2):
                if node.index < node2.index:
                    f.attr("edge", arrowhead="none")
                    f.edge(nodeName, node2Name, "Cost = {}".format(cost) if showCost else None)
                    f.attr("edge", arrowhead="normal")
            else:
                f.edge(nodeName, node2Name, "Cost = {}".format(cost) if showCost else None)

    # Draw Path
    f.attr("edge", color="red")
    for i in range(len(path) - 1):
        node = path[i]
        node2 = path[i + 1]
        nodeName = str(node.data) if not node.defaultName else "Node {}".format(node.data)
        node2Name = str(node2.data) if not node2.defaultName else "Node {}".format(node2.data)
        f.edge(nodeName, node2Name, "{}".format(i + 1))

    print("Rendered to " + f.render())

"""
Grid 0 = free, 1 = obs
"""
def graphFromGrid(grid, includeUnconnected=False):
    numNodes = len(grid) * len(grid[0])
    nodesGrid = []
    graph = AdjacencyMatrixGraph(numNodes)
    graph.nodes = []
    for i in range(len(grid)):
        nodesGrid.append([])
        nodesList = nodesGrid[-1]

        for j in range(len(grid[0])):
            if grid[i][j] == 0 or includeUnconnected:
                node = Node(data=str((i, j)))
                graph.nodes.append(node)
                nodesList.append(node)
            else:
                nodesList.append(None)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                if i > 0 and grid[i - 1][j] == 0:
                    graph.addEdge(nodesGrid[i][j], nodesGrid[i - 1][j])

                if i < len(grid) - 1 and grid[i + 1][j] == 0:
                    graph.addEdge(nodesGrid[i][j], nodesGrid[i + 1][j])

                if j > 0 and grid[i][j - 1] == 0:
                    graph.addEdge(nodesGrid[i][j], nodesGrid[i][j - 1])

                if j < len(grid[0]) - 1 and grid[i][j + 1] == 0:
                    graph.addEdge(nodesGrid[i][j], nodesGrid[i][j + 1])

    # Function hack
    graph.getNodeByCoords = lambda a, b: nodesGrid[a][b]
    graph.visualizeGraphWithPath = partial(visualizeGraphWithPath, graph)
    graph.visualizeGraph = partial(visualizeGraph, graph)

    return graph, nodesGrid
