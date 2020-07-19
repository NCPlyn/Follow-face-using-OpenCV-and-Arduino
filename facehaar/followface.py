import serial
import struct
import cv2
import sys
import logging as log
import datetime as dt
from time import sleep

camnum = 0
debug = "n"
ardport = "COM9"

arguments = len(sys.argv) - 1
if(arguments == 1):
    print("Using config")
    with open(sys.argv[1]) as fp:
        ardport = fp.readline().strip()
        camnum = fp.readline().strip()
        debug = fp.readline().strip()
else:
    print("something is wrong, i can feel it, enter values manually")
    print("Arduino port: ")
    ardport = input()
    print("Camera number: ")
    camnum = input()
    print("Debug[y/n]: ")
    debug = input()

ser = serial.Serial(ardport, 2000000)
sleep(1)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(int(camnum))
video_capture.set(3, 640)
video_capture.set(4, 480)
anterior = 0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(1)
        pass

    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(30, 30)
    )

    cv2.imshow('Video', frame)

    for (x, y, w, h) in faces:
        halfw = w/2
        halfh = h/2
        centerx = int(x+halfw)
        centery = int(y+halfh)
        if(debug == "y"):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.rectangle(frame, (centerx-1, centery-1), (centerx+1, centery+1), (0, 255, 0), 4)
            cv2.rectangle(frame, (320, 240), (320, 240), (0, 0, 255), 4)
        idkx = 320-centerx
        idky = 240-centery
        if idkx < 20 and idkx > -20:
            xN = 0
        elif idkx < -20:
            xN = 1
        elif idkx > 20:
            xN = 2
        if idky < 20 and idky > -20:
            yN = 0
        elif idky < -20:
            yN = 1
        elif idky > 40:
            yN = 2
        toSend = "1" + str(xN) + str(yN)
        ser.write(str(toSend).encode()) 
        ser.readline()
	
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser.close()
        break

    cv2.imshow('Video', frame)

video_capture.release()
cv2.destroyAllWindows()