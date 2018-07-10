import cv2
from threading import Thread

class WebcamVideoStream:
    def __init__(self, src=3):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, 960)
        self.stream.set(4, 540)
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
