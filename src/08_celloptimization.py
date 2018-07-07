import numpy as np
import math
import time
import cv2
from AdjacencyMatrixGraph import AdjacencyMatrixGraph
from Graph import Node
import bisect

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
startPoint = (120, 400)
endPoint = (475, 100)

DIST_FUNC = 1 # 0 = X-coord, 1 = Euclidian

map = np.zeros((mapSize, mapSize, 3), dtype=np.uint8)

robotSize = int(round(20.0 * math.sqrt(2.0)))
robotMargin = 0

cSpaceGrowth = robotSize + robotMargin

# y1, x1, y2, x2
obstacles = [
    [100, 100, 250, 250],
    [400, 220, 450, 380],
    #[360, 350, 450, 450],
    [100, 350, 220, 420]
]

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

def strToTuple(string):
    x, y = string.replace("(", "").replace(")", "").replace(" ", "").split(",")
    x = int(x)
    y = int(y)
    return (x, y)

# Grow Obstacles
cSpaceObstacles = []
for x1, y1, x2, y2 in obstacles:
    cSpaceObstacles.append([max(x1 - cSpaceGrowth, 0), max(y1 - cSpaceGrowth, 0), min(x2 + cSpaceGrowth, mapSize - 1), min(y2 + cSpaceGrowth, mapSize - 1)])

# Render Obstacles
for x1, y1, x2, y2 in cSpaceObstacles:
    map[x1:x2, y1:y2] = (95, 112, 255)

for x1, y1, x2, y2 in obstacles:
    map[x1:x2, y1:y2] = (30, 60, 255)

cv2.imshow("C-Space Obstacles", map)

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
    print(obsEdges[x])
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

nodes = {}
edges = [] # (node1, node2, cost)

def addExtraneousPoint(extraneousPoint):
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
                nodes[str((x1, y1))] = Node(data=str((x1, y1)))
                returnNode = nodes[str((x1, y1))]

            if str((x2, y2)) not in nodes:
                nodes[str((x2, y2))] = Node(data=str((x2, y2)))

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


startNode = addExtraneousPoint(startPoint)

for i in range(len(xCoordsFreeEdges) - 1):
    x1 = xCoordsFreeEdges[i]
    x2 = xCoordsFreeEdges[i + 1]
    print(x1, x2)

    for edge1 in freeEdges[x1]:
        for edge2 in freeEdges[x2]:
            y1 = int((edge1[0] + edge1[1]) / 2.0)
            y2 = int((edge2[0] + edge2[1]) / 2.0)

            if str((x1, y1)) not in nodes:
                nodes[str((x1, y1))] = Node(data=str((x1, y1)))

            if str((x2, y2)) not in nodes:
                nodes[str((x2, y2))] = Node(data=str((x2, y2)))

            if not containObstacle(x1, x2, y1, y2):
                if DIST_FUNC == 0:
                    distance = abs(x2 - x1) # Only x-dist
                else:
                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) # x and y dist

                edges.append((nodes[str((x1, y1))], nodes[str((x2, y2))], distance))

                cv2.line(map, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.circle(map, (x1, y1), 8, (255, 0, 255), -1)
                cv2.circle(map, (x2, y2), 8, (255, 0, 255), -1)

endNode = addExtraneousPoint(endPoint)

nodeObjects = nodes.values()
graph = AdjacencyMatrixGraph(len(nodes))
graph.nodes = nodeObjects

for node1, node2, cost in edges:
    graph.addEdge(node1, node2, cost=cost, directed=False)

path = graph.dijsktraSearch(startNode, endNode)

for i in range(len(path) - 1):
    pt1 = path[i].data
    pt2 = path[i + 1].data
    cv2.line(map, strToTuple(pt1), strToTuple(pt2), (0, 255, 0), 2)

graph.visualizeGraphWithPath(path)

cv2.imshow("Obstacle Edges", cv2.resize(map, (0, 0), fx=2.0, fy=2.0))

cv2.waitKey(50000000)
