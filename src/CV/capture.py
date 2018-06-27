import cv2

cap = cv2.VideoCapture(2)
cap.set(3, 480)
cap.set(4, 270)
i = 135353535353535353535353535353535353535353535353535
while True:
    img = cap.read()[1]
    print(img.shape)
    cv2.imshow("img", img)
    cv2.waitKey(25)
    global i
    i = i + 1
    cv2.imwrite("img"+str(i)+".jpg", img)
