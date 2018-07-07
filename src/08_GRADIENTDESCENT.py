import numpy as np
import math
import time
import copy
import cv2
from AdjacencyMatrixGraph import AdjacencyMatrixGraph
from Graph import Node
import bisect
import matplotlib
matplotlib.use("Agg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

random.seed(1337)

class Cell:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

    def bounding(self, other):
        if self.y1 < other.y1 and self.y2 < other.y1:
            return 0
        if self.y1 > other.y2 and self.y2 > other.y2:
            return 0

        if self.x1 == other.x2:
            return 1
        if self.x2 == other.x1:
            return 2

        return 0

# millimeter grid
# origin (bottom left) = (0, 0) top right = (500, 500)

mapSize = 500
startPoint = (450, 450)
endPoint = (20, 20)

DIST_FUNC = 1 # 0 = X-coord, 1 = Euclidian

map = np.zeros((mapSize, mapSize, 3), dtype=np.uint8)

robotSize = int(round(20.0 * math.sqrt(2.0)))
robotMargin = 0

cSpaceGrowth = robotSize + robotMargin

# y1, x1, y2, x2
"""obstacles = [
    [100, 100, 250, 250],
    [400, 220, 450, 380],
    #[360, 350, 450, 450],
    [100, 300, 220, 420]
]"""

obstacles = []
for i in range(8):
    obstacleX = random.randint(100, 400)
    obstacleY = random.randint(100, 400)
    obstacles.append([obstacleX, obstacleY, obstacleX + random.randint(1, 40), obstacleY + random.randint(1, 40)])


def betweenNodes(obstacle, x1, x2, y1, y2):
    _y1 = min(y1, y2)
    _y2 = max(y1, y2)
    _x1 = min(x1, x2)
    _x2 = max(x1, x2)

    if (obstacle[0] > y2 and obstacle[2] < y1) or (obstacle[0] > y1 and obstacle[2] < y2): # or (obstacle[3] > y1 and obstacle[1] < y2):
        if (obstacle[1] > x1 and obstacle[3] < x2) or (obstacle[3] > x1 and obstacle[1] < x2):
            return True

    return False

def containObstacle(x1, x2, y1, y2):
    for obs in cSpaceObstacles:
        if betweenNodes(obs, x1, x2, y1, y2):
            return True

    return False

def strTo4Tuple(string):
    x, y, ymin, ymax = string.replace("(", "").replace(")", "").replace(" ", "").split(",")
    x = int(x)
    y = int(y)
    ymin = int(ymin)
    ymax = int(ymax)
    return (x, y, ymin, ymax)

# Grow Obstacles
cSpaceObstacles = []
for x1, y1, x2, y2 in obstacles:
    cSpaceObstacles.append([max(x1 - cSpaceGrowth, 0), max(y1 - cSpaceGrowth, 0), min(x2 + cSpaceGrowth, mapSize - 1), min(y2 + cSpaceGrowth, mapSize - 1)])

# Render Obstacles
for x1, y1, x2, y2 in cSpaceObstacles:
    map[x1:x2, y1:y2] = (95, 112, 255)

for x1, y1, x2, y2 in obstacles:
    map[x1:x2, y1:y2] = (30, 60, 255)

#cv2.imshow("C-Space Obstacles", map)

# Find edges {x: [y1, y2]}

obsEdges = {}

for y1, x1, y2, x2 in cSpaceObstacles:
    if x1 not in obsEdges:
        obsEdges[x1] = []

    if x2 not in obsEdges:
        obsEdges[x2] = []

    obsEdges[x1].append((y1, y2))
    obsEdges[x2].append((y1, y2))

for x in obsEdges:
    #print(obsEdges[x])
    for y1, y2 in obsEdges[x]:
        cv2.line(map, (x, y1), (x, y2), (0, 255, 0), 3)

freeEdges = {}

for x in obsEdges:
    obsPairs = []
    for y1, x1, y2, x2 in cSpaceObstacles:
        if x > x1 and x < x2 or x < x1 and x > x2:
            obsPairs.append((y1, y2))

    for y1, y2 in obsPairs:
        cv2.line(map, (x, y1), (x, y2), (255, 255, 0), 3)

    obsPairs = obsPairs + obsEdges[x]

    lineArr = np.zeros(mapSize)
    for y1, y2 in obsPairs:
        lineArr[y1:y2] = 1

    edges = np.where(np.abs(np.diff(np.concatenate(([0], np.equal(lineArr, 0).view(np.int8), [0])))) == 1)[0].reshape(-1, 2)

    for y1, y2 in edges:
        cv2.line(map, (x, y1), (x, y2), (0, 255, 255), 3)

    freeEdges[x] = edges

xCoordsFreeEdges = sorted(freeEdges.keys())

# node format = (x, y, ymin, ymax)
nodes = {}
edges = [] # (node1, node2, cost)

def addExtraneousPoint(extraneousPoint, minY=None, maxY=None):
    x1 = extraneousPoint[0]
    startSides = []

    if x1 < xCoordsFreeEdges[0]:
        startSides.append(xCoordsFreeEdges[0])
    elif x1 > xCoordsFreeEdges[-1]:
        startSides.append(xCoordsFreeEdges[-1])
    else:
        pt = bisect.bisect_left(xCoordsFreeEdges, x1)
        startSides.append(xCoordsFreeEdges[pt - 1])
        startSides.append(xCoordsFreeEdges[pt])

    returnNode = None

    for x2 in startSides:
        for edge in freeEdges[x2]:
            y1 = extraneousPoint[1]
            y2 = int((edge[0] + edge[1]) / 2.0)

            if str((x1, y1)) not in nodes:
                if minY is  None:
                    minY = y1
                if maxY is None:
                    maxY = y1

                nodes[str((x1, y1))] = Node(data=str((x1, y1, minY, maxY)))
                returnNode = nodes[str((x1, y1))]

            if str((x2, y2)) not in nodes:
                nodes[str((x2, y2))] = Node(data=str((x2, y2, min(edge), max(edge))))

            if x1 > x2:
                _x1, _x2 = x2, x1
            else:
                _x1, _x2 = x1, x2

            if not containObstacle(_x1, _x2, y1, y2):
                if DIST_FUNC == 0:
                    distance = abs(x2 - x1) # Only x-dist
                else:
                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) # x and y dist

                edges.append((nodes[str((x1, y1))], nodes[str((x2, y2))], distance))

                cv2.line(map, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.circle(map, (x1, y1), 8, (255, 0, 255), -1)
                cv2.circle(map, (x2, y2), 8, (255, 0, 255), -1)

    return returnNode

mapForRender = np.copy(map)

startNode = addExtraneousPoint(startPoint)

for i in range(len(xCoordsFreeEdges) - 1):
    x1 = xCoordsFreeEdges[i]
    x2 = xCoordsFreeEdges[i + 1]
    #print(x1, x2)

    for edge1 in freeEdges[x1]:
        for edge2 in freeEdges[x2]:
            y1 = int((edge1[0] + edge1[1]) / 2.0)
            y2 = int((edge2[0] + edge2[1]) / 2.0)

            if str((x1, y1)) not in nodes:
                nodes[str((x1, y1))] = Node(data=str((x1, y1, min(edge1), max(edge1))))

            if str((x2, y2)) not in nodes:
                nodes[str((x2, y2))] = Node(data=str((x2, y2, min(edge2), max(edge2))))

            if not containObstacle(x1, x2, y1, y2):
                if DIST_FUNC == 0:
                    distance = abs(x2 - x1) # Only x-dist
                else:
                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) # x and y dist

                edges.append((nodes[str((x1, y1))], nodes[str((x2, y2))], distance))

                cv2.line(map, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.circle(map, (x1, y1), 8, (255, 0, 255), -1)
                cv2.circle(map, (x2, y2), 8, (255, 0, 255), -1)

if mapSize - 1 not in xCoordsFreeEdges and mapSize not in xCoordsFreeEdges:
    addExtraneousPoint((mapSize - 1, mapSize / 2), minY = 0, maxY = mapSize - 1)

endNode = addExtraneousPoint(endPoint)

nodeObjects = nodes.values()
graph = AdjacencyMatrixGraph(len(nodes))
graph.nodes = nodeObjects

for node1, node2, cost in edges:
    graph.addEdge(node1, node2, cost=cost, directed=False)

path = graph.dijsktraSearch(startNode, endNode)
graph.visualizeGraphWithPath(path)

#graph.visualizeGraph()
cv2.imshow("Obstacle Edges", cv2.resize(map, (0, 0), fx=2.0, fy=2.0))
cv2.waitKey(5000000)
path = [strTo4Tuple(elem.data) for elem in path]

# ------ NO GRAPH CODE BELOW THIS POINT ------

def renderPathOntoImage(newPath):
    global mapForRender
    newMap = np.copy(mapForRender)

    for i in range(len(path) - 1):
        x1, y1, ymin1, ymax1 = newPath[i]
        x2, y2, ymin2, ymax2 = newPath[i + 1]

        cv2.line(newMap, (x1, ymin1), (x1, ymax1), (255, 0, 125), 2)
        cv2.circle(newMap, (x1, y1), 8, (0, 255, 0), -1)

        cv2.line(newMap, (x2, ymin2), (x2, ymax2), (255, 0, 125), 2)
        cv2.circle(newMap, (x2, y2), 8, (0, 255, 0), -1)

        cv2.line(newMap, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return cv2.resize(newMap, (0, 0), fx=2.0, fy=2.0)

def createPath(_yVec):
    newPath = copy.deepcopy(path)

    for i in range(len(_yVec)):
        o = newPath[i + 1]
        newPath[i + 1] = (o[0], int(round(_yVec[i])), o[2], o[3])

    return newPath


startNode = path[0]
endNode = path[-1]
ptsPath = path[1:-1]

fx1 = abs(startNode[0] - ptsPath[0][0])
fy1 = startNode[1]

fx2 = abs(endNode[0] - ptsPath[-1][0])
fy2 = endNode[1]

xVec = np.array([point[0] for point in ptsPath])
xVec = np.ediff1d(xVec)

yVec = np.array([point[1] for point in ptsPath]) # Initial Value Only
numElements = len(yVec)

yMinVec = np.array([point[2] for point in ptsPath])
yMaxVec = np.array([point[3] for point in ptsPath])

def loss(_yVec):
    global fx1, fx2, fy1, fy2, numElements, xVec

    lossSum = 0
    for i in range(numElements - 1):
        lossSum = lossSum + math.sqrt(float(xVec[i]) ** 2 + float(_yVec[i + 1] - _yVec[i]) ** 2)

    lossSum = lossSum + math.sqrt(float(fx1) ** 2 + float(_yVec[0] - fy1) ** 2)

    lossSum = lossSum + math.sqrt(float(fx2) ** 2 + float(_yVec[-1] - fy2) ** 2)

    return lossSum

def derivativeTerm(_xDist, _y, _yNext):
    return (_yNext - _y) / math.sqrt(_xDist ** 2 + (_yNext - _y) ** 2)

def lossPartialGradient(_yVec, i):
    if i == 0:
        return derivativeTerm(fx1, fy1, _yVec[i]) + derivativeTerm(xVec[i], _yVec[i + 1], _yVec[i])
    elif i == len(_yVec) - 1:
        return derivativeTerm(xVec[i - 1], _yVec[i - 1], _yVec[i]) + derivativeTerm(fx2, fy2, _yVec[i])
    else:
        return derivativeTerm(xVec[i - 1], _yVec[i - 1], _yVec[i]) + derivativeTerm(xVec[i], _yVec[i + 1], _yVec[i])

def lossGradient(_yVec):
    return np.array([lossPartialGradient(_yVec, i) for i in range(len(_yVec))])

print(loss(yVec))

# Assumes only 2 elements in yVec
"""
graph_min1 = yMinVec[0]
graph_max1 = yMaxVec[0]

graph_min2 = yMinVec[1]
graph_max2 = yMaxVec[1]

graph_x = np.linspace(graph_min1, graph_max1, 50)
graph_y = np.linspace(graph_min2, graph_max2, 50)

graph_xs = np.zeros(len(graph_x) * len(graph_y))
graph_ys = np.zeros(len(graph_x) * len(graph_y))
graph_zs = np.zeros(len(graph_x) * len(graph_y))
graph_zs2 = np.zeros(len(graph_x) * len(graph_y))

i = 0
for xPoint in graph_x:
    for yPoint in graph_y:
        graph_xs[i] = xPoint
        graph_ys[i] = yPoint
        graph_zs2[i] = loss(np.array([xPoint, yPoint])) # lossGradient(np.array([xPoint, yPoint]))[0]
        graph_zs[i] = lossGradient(np.array([xPoint, yPoint]))[0]
        i = i + 1

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(graph_xs, graph_ys, graph_zs)

minIndex = np.argmin(graph_zs2)
minX = graph_xs[minIndex]
minY = graph_ys[minIndex]
minZ = graph_zs[minIndex]

print(minX, minY)
ax.plot([minX], [minY], [minZ], markerfacecolor="k", marker='o', markersize=5)
plt.show()
"""
cv2.imshow("Original Path", renderPathOntoImage(path))
cv2.waitKey(50000000)


#print(path)
#print("")
#print(newPath)
#print("")

newYVec = yVec
cv2.namedWindow("Path Optimized")
cv2.namedWindow("Loss History")

lossHistory = []
learningRate = 1.5
numSteps = 600

# TODO define stopping conditions
for step in range(numSteps / 5):
    for i in range(5):
        newYVec = newYVec - learningRate * lossGradient(newYVec)

        # Limit Values
        for i in range(len(newYVec)):
            newYVec[i] = min(newYVec[i], yMaxVec[i])
            newYVec[i] = max(newYVec[i], yMinVec[i])

        lossHistory.append(loss(newYVec))

    newPath = createPath(newYVec)
    print("Step = ", step * 5 , " Loss = ", loss(newYVec), " Gradient = ", lossGradient(newYVec))
    cv2.imshow("Path Optimized", renderPathOntoImage(newPath))

    # Graph Loss over Time
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_title("Path Optimization")
    ax.set_xlabel("Num Optimization Steps")
    ax.set_ylabel("Optimization Loss (Path Length)")

    plt.plot(lossHistory)
    plt.savefig("lossHistory.png")

    graph = cv2.imread("lossHistory.png")
    cv2.imshow("Loss History", graph)

    cv2.waitKey(30)

cv2.imshow("Path Optimized", renderPathOntoImage(newPath))

cv2.waitKey(5000000)
