import numpy as np
import math
from scipy.signal import convolve2d
from Queue import PriorityQueue
import time
import cv2

def manhattanDist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

time1 = 0
time2 = 0
time3 = 0
time4 = 0

def aStar(start, goal, occupancyGrid):
    global time1, time2, time3, time4
    t = time.time()
    availPoints = PriorityQueue()
    availPoints.put((0, start))

    prev = {}
    costToPoint = {}

    prev[start] = None
    costToPoint[start] = 0
    time1 = time1 + (time.time() - t)
    t = time.time()

    while not availPoints.empty():
        nextPoint = availPoints.get()[1]

        if nextPoint == goal:
            break

        pts = [
            (nextPoint[0] + 1, nextPoint[1] + 0),
            (nextPoint[0] - 1, nextPoint[1] + 0),
            (nextPoint[0] + 0, nextPoint[1] + 1),
            (nextPoint[0] + 0, nextPoint[1] - 1)
        ]

        pts = [pt for pt in pts if pt[0] < occupancyGrid.shape[0] and pt[1] < occupancyGrid.shape[1] and pt[0] > -1 and pt[1] > -1 and occupancyGrid[pt[0]][pt[1]] == 0]

        for pt in pts:
            cost = costToPoint[nextPoint] + 1
            if (pt not in costToPoint.keys()) or (cost < costToPoint[pt]):
                costToPoint[pt] = cost
                p = cost + manhattanDist(goal, pt)
                availPoints.put((p, pt))
                prev[pt] = nextPoint

    time2 = time2 + (time.time() - t)
    t = time.time()
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])

    path = path[::-1]

    time3 = time3 + (time.time() - t)

    return path

# millimeter grid
# origin (bottom left) = (0, 0) top right = (500, 500)

robotSize = int(round(20.0 * math.sqrt(2.0)))
robotMargin = 0

# x1, y1, x2, y2
obstacles = [
    [100, 100, 250, 250],
    [350, 220, 400, 450],
    [0, 350, 320, 420]
]

size = 500
ratio = 5
grid = np.zeros((size, size))

for x1, y1, x2, y2 in obstacles:
    grid[x1:x2, y1:y2] = 1

convSize = 2 * (robotMargin + robotSize) + 1
convMatrix = np.zeros((convSize, convSize))
convMatrix[:, :] = 1

cSpaceGrid = convolve2d(grid, convMatrix, mode="same")
cSpaceGrid = np.divide(cSpaceGrid, np.amax(cSpaceGrid))
print([i for i in cSpaceGrid[200]])

smallerGrid = np.zeros((size/ratio, size/ratio))

for i in range(size/ratio):
    for j in range(size/ratio):
        section = cSpaceGrid[i*ratio:i*ratio+ratio, j*ratio:j*ratio+ratio]
        if np.count_nonzero(section) > ratio:
            smallerGrid[i][j] = 1
        else:
            smallerGrid[i][j] = 0


start = (25, 225)
end = (60, 480)

path = aStar((start[0] / ratio, start[1] / ratio), (end[0] / ratio, end[1] / ratio), smallerGrid)

cSpaceGridDisplay = cSpaceGrid * 150 + 100
cSpaceGridDisplay[cSpaceGridDisplay < 101] = 0
image = np.stack([cSpaceGridDisplay] * 3, axis=2)

prevX = start[1]
prevY = start[0]
for y, x in path:
    x = int(x * ratio + ratio / 2)
    y = int(y * ratio + ratio / 2)
    cv2.line(image, (prevX, prevY), (x, y), (0, 255, 0))
    prevX = x
    prevY = y

cv2.imwrite("smaller.png", smallerGrid * 255)

cv2.imwrite("output.png", image)

#for i in range(size/ratio):
#    str = "|"
#    for j in range(size/ratio):
#        char = " "
#        if smallerGrid[i][j] == 1:
#            char = "O"
#        if (i, j) in path:
#            char = "&"
#        str = str + char
#
#    str = str + "|"
#    print(str)
#
#print()
#
#print(time1, time2, time3)
