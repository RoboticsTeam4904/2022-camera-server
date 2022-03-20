PATH = 'image_stream.jpg'
FRAMERATE = 6

import cv2 as cv
from time import sleep
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("urbadgetgoodvidded")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("something died i guess")
        break

    cv.imwrite(PATH, frame)
    print("wrote image")

    sleep(1/FRAMERATE)


