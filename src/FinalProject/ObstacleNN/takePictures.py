import cv2
import sys
cap = cv2.VideoCapture(int(sys.argv[1]))
cap.set(3, 640)
cap.set(4, 360)

i = 0
while True:
    img = cap.read()[1]

    cv2.imshow("Image", img)
    if cv2.waitKey(20) != -1:
        i = i + 1
        cv2.imwrite("image{}.png".format(i), img)
        print("Saved as image{}.png".format(i))
