# python3 followface.py example.txt
# import the necessary packages
from imutils.video import VideoStream
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import cv2
import serial
import sys
import numpy

arguments = len(sys.argv) - 1
if(arguments == 1):
	print("[INFO] Using config...")
	with open(sys.argv[1]) as fp:
		ardport = fp.readline().strip()
		camnum = int(fp.readline().strip())
		showoutput = int(fp.readline().strip())
else:
	print("[WARN] No config specified, please enter vaulues manually:")
	print("Arduino port: (like \"/dev/ttyUSB0\")")
	ardport = input()
	print("Camera number:")
	camnum = int(input())
	print("Show slow output:")
	showoutput = int(input())

#connect to arduino
print("[INFO] connecting to arduino...")
ser = serial.Serial(ardport, 2000000)
time.sleep(0.5)

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=camnum).start()
time.sleep(0.5)

# FPS stuff
framestotal = 0
start = time.time()
fps = 0

# for tracing only one face
detectedfaces = 0
oldFaceX = 0
oldFaceY = 0
faceeX = []
faceeY = []
xylist = []

# calculation and writing to arduino over serial
def arduinowrite(idky,idkx):
    xN = 0
    yN = 0
    if idkx < 30 and idkx > -30:
    	xN = 0
    elif idkx < -30:
    	xN = 1
    elif idkx > 30:
    	xN = 2
    if idky < 30 and idky > -30:
    	yN = 0
    elif idky < -30:
    	yN = 1
    elif idky > 40:
    	yN = 2
    toSend = "1" + str(xN) + str(yN)
    ser.write(str(toSend).encode())
    ser.flush()

# class for faces array
class centerpoint(object):
    def __init__(self, xpos,ypos,centerx,centery):
        self.xpos = xpos
        self.ypos = ypos
        self.centerx = centerx
        self.centery = centery

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=800)
 
	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
 
	# pass the blob through the network and obtain the detections and predictions
	net.setInput(blob)
	detections = net.forward()
    
	# FPS calculation
	if(framestotal == 30):
		end = time.time()
		seconds = end - start
		fps  = 30 / seconds
		framestotal = 0
		start = time.time()

	cv2.putText(frame, "FPS: " + str('{0:.2f}'.format(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
		if confidence < 0.4:
			continue

		# compute the (x, y)-coordinates of the bounding box for the object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
 
		# draw the bounding box of the face along with the associated probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
		cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

		centerx = int(startX+((endX-startX)/2)) # calculate center of face in X
		centery = int(startY+((endY-startY)/2)) # calculate center of face in Y
		cv2.rectangle(frame, (centerx-1, centery-1), (centerx+1, centery+1), (0, 255, 0), 4) # draw face center point
		hscw = int(w/2)
		hsch = int(h/2)
		cv2.rectangle(frame, (hscw, hsch), (hscw, hsch), (0, 0, 255), 4) # draw center point of screen
		
		idkx = (w/2)-centerx # difference between center of screen & face in X
		idky = (h/2)-centery # difference between center of screen & face in Y

		detectedfaces += 1 # add to number of detected faces in frame
        
		xylist.append(centerpoint(idkx, idky, centerx, centery)) # append face coords to array

	
	if(detectedfaces == 1):
		arduinowrite(xylist[0].ypos,xylist[0].xpos) # if only one face detected, call function to control arduino
	elif(detectedfaces > 1):
		for obj in xylist: # append center points of faces to arrays
			faceeX.append(obj.centerx)
			faceeY.append(obj.centery)

		# select the closest value and return index
		bestFaceX = min(range(len(faceeX)), key=lambda i: abs(faceeX[i]-oldFaceX))
		bestFaceY = min(range(len(faceeY)), key=lambda i: abs(faceeY[i]-oldFaceY))
        
		# get centerpoints from the indexes
		oldFaceX = xylist[bestFaceX].centerx
		oldFaceY = xylist[bestFaceY].centery
		
		arduinowrite(xylist[bestFaceY].ypos,xylist[bestFaceX].xpos) # call function to control arduino
        
		# clear out the arrays
		faceeX.clear()
		faceeY.clear()

	# clear array with faces
	xylist.clear()
    
	# show number of detected faces on screen
	cv2.putText(frame, "Faces: " + str(detectedfaces), (685, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	detectedfaces = 0
    
	framestotal += 1 # add 1 to processed frames
    
	# show the output frame
	if(showoutput == 1):
		if(framestotal == 1):
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
			# if the 'e' key was pressed, change show method
			if key == ord("e"):
				if(showoutput == 1):
					showoutput = 0
				else:
					showoutput = 1
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
	else:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the 'e' key was pressed, change show method
		if key == ord("e"):
			if(showoutput == 1):
				showoutput = 0
			else:
				showoutput = 1
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
