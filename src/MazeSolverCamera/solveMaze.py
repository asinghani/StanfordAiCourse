import cv2
from capMaze import getMazeData
import queue

lastFoundImg = None

def solveMaze(img, x):
    global lastFoundImg
    mazeTopView, accessGrid = getMazeData(img, x)
    if accessGrid is None:
        lastFoundImg = mazeTopView
        return
    if accessGrid == []:
        return

    print(accessGrid)

    start = (0, 0)
    end = (3, 2)

    # 0 = left, 1 = right, 2 = up, 3 = down
    def getAvailableLocations(x, y):
        dirs = accessGrid[y][x]
        locations = []
        if 0 in dirs:
            locations.append((x-1, y))
        if 1 in dirs:
            locations.append((x+1, y))
        if 2 in dirs:
            locations.append((x, y-1))
        if 3 in dirs:
            locations.append((x, y+1))
        return locations

    currPoint = start
    unvisitedQueue = queue.PriorityQueue()
    visited = []
    path = []

    while currPoint != end:
        visited.append(currPoint)
        path.append(currPoint)
        locations = getAvailableLocations(currPoint[0], currPoint[1])
        locations = list(filter(lambda a: a not in visited, locations))
        if locations.__len__() == 0:
            loc = unvisitedQueue.get(False)
            if loc == None:
                print("err")
                break
            path = path[:path.index(loc[1][0])+1]
            loc = loc[1][1]
        elif locations.__len__() == 1:
            loc = locations[0]
        else:
            loc = locations[0]
            locations = locations[1:]
            x = 0
            for i in locations:
                x = x + 1
                unvisitedQueue.put((-1 * (path.__len__() + x), [currPoint, i]))

        currPoint = loc
    path.append(end)

    # 0 = left, 1 = right, 2 = up, 3 = down
    heading = 1

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

    # 0 = right turn, 1 = left turn, 2 = fwd
    cmds = []
    prev = None
    for i in range(len(path)):
        cv2.putText(mazeTopView, str(i), (175 + path[i][0] * 250, 175 + path[i][1] * 250), cv2.FONT_HERSHEY_SIMPLEX, 1, 128, 1)
        if prev:
            lastHeading = heading
            heading = getHeadingFromPoints(prev, path[i])
            if heading == lastHeading:
                pass
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

            cmds.append(2)

        prev = path[i]

    print(cmds)

    cv2.imshow("maze", mazeTopView)

cap = cv2.VideoCapture(2)
cap.set(3, 960)
cap.set(4, 540)
while True:
    img = cap.read()[1]
    cv2.imshow("img", cv2.resize(img, (480, 270)))
    solveMaze(img, False)
    if not (lastFoundImg is None):
        cv2.imshow("found paper", cv2.resize(lastFoundImg, (480, 270)))

    if cv2.waitKey(50) == 13 and not (lastFoundImg is None):
        solveMaze(lastFoundImg, True)
        cv2.waitKey(3000)
