import random
from GridGraph import graphFromGrid
from AdjacencyMatrixGraph import AdjacencyMatrixGraph as Graph
from Graph import Node

# random.seed(1337)

# size = 15
g = Graph(7)

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6

g.nodes = [Node(data="A"),
           Node(data="B"),
           Node(data="C"),
           Node(data="D"),
           Node(data="E"),
           Node(data="F"),
           Node(data="G")]

g.addEdge(A, B, directed=True)
g.addEdge(A, C, directed=True)

g.addEdge(B, A, directed=True)
g.addEdge(B, C, directed=True)
g.addEdge(B, D, directed=True)
g.addEdge(B, E, directed=True)

g.addEdge(C, A, directed=True)
g.addEdge(C, B, directed=True)
g.addEdge(C, D, directed=True)
g.addEdge(C, G, directed=True)

g.addEdge(D, B, directed=True)
g.addEdge(D, C, directed=True)
g.addEdge(D, E, directed=True)
g.addEdge(D, G, directed=True)

g.addEdge(E, B, directed=True)
g.addEdge(E, D, directed=True)
g.addEdge(E, F, directed=True)
g.addEdge(E, G, directed=True)

g.addEdge(F, E, directed=True)
g.addEdge(F, G, directed=True)

g.addEdge(G, C, directed=True)
g.addEdge(G, D, directed=True)
g.addEdge(G, E, directed=True)
g.addEdge(G, F, directed=True)


pathNodes = g.aStar(g.getAllNodes()[A], g.getAllNodes()[G])
g.visualizeGraphWithPath(pathNodes)

paths = g.multiBfs(g.getAllNodes()[A], g.getAllNodes()[G])
print(len(paths))
for path in paths:
    print(path)

import sys
sys.exit(0)

grid = [[0, 1, 1],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]]

g, nodesGrid = graphFromGrid(grid, includeUnconnected=True)

path = []
for node in pathNodes:
    x, y = node.data.replace("(", "").replace(")", "").replace(" ", "").split(",")
    x = int(x)
    y = int(y)
    path.append((x, y))

# 0 = left, 1 = right, 2 = up, 3 = down
heading = 0

def getHeadingFromPoints(pt1, pt2):
    if pt1[1] > pt2[1]:
        return 2
    elif pt1[1] < pt2[1]:
        return 3
    else:
        if pt1[0] > pt2[0]:
            return 0
        else:
            return 1

# 0 = left turn, 1 = right turn, 2 = fwd
cmds = []
prev = None
for i in range(len(path)):
    if prev:
        lastHeading = heading
        heading = getHeadingFromPoints(prev, path[i])
        if heading == lastHeading:
            cmds.append(2)
        else:
            if lastHeading == 0:
                if heading == 2:
                    cmds.append(0)
                if heading == 3:
                    cmds.append(1)

            if lastHeading == 1:
                if heading == 2:
                    cmds.append(1)
                if heading == 3:
                    cmds.append(0)

            if lastHeading == 2:
                if heading == 1:
                    cmds.append(0)
                if heading == 0:
                    cmds.append(1)

            if lastHeading == 3:
                if heading == 1:
                    cmds.append(1)
                if heading == 0:
                    cmds.append(0)

    prev = path[i]

print(cmds)
