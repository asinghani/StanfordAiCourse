import random
from GridGraph import graphFromGrid

# random.seed(1337)

# size = 15
# g = Graph(size)

# for i in range(random.randint(size * 5, size * 6)):
#     g.addEdge(random.randint(0, size - 1), random.randint(0, size - 1), cost=random.randint(10, 40), directed=False)

# path = g.dijsktraSearch(g.getAllNodes()[0], g.getAllNodes()[4])

grid = [[0, 1, 1],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]]

g, nodesGrid = graphFromGrid(grid, includeUnconnected=True)
pathNodes = g.dijsktraSearch(g.getNodeByCoords(3, 0), g.getNodeByCoords(0, 0))
g.visualizeGraphWithPath(pathNodes, showCost=True)

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
