# USAGE
# sudo python3 detect_faces_video.py example.txt

# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import serial
import sys

arguments = len(sys.argv) - 1
if(arguments == 1):
	print("[INFO] Using config...")
	with open(sys.argv[1]) as fp:
		ardport = fp.readline().strip()
		camnum = fp.readline().strip()
else:
	print("[WARN] No config specified, please enter vaulues manually:")
	print("Arduino port: (like \"/dev/ttyUSB0\")")
	ardport = input()
	print("Camera number:")
	camnum = input()

#connect to arduino
print("[INFO] connecting to arduino...")
ser = serial.Serial(ardport, 2000000)
time.sleep(1)

#optimalize cv2
cv2.setUseOptimized(True)

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=int(camnum)).start()
time.sleep(1)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=800)
 
	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))
 
	# pass the blob through the network and obtain the detections and predictions
	net.setInput(blob)
	detections = net.forward()

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
		cv2.rectangle(frame, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
		cv2.putText(frame, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
			
		#draw center points
		centerx = int(startX+((endX-startX)/2))
		centery = int(startY+((endY-startY)/2))
		cv2.rectangle(frame, (centerx-1, centery-1), (centerx+1, centery+1), (0, 255, 0), 4)
		hscw = int(w/2)
		hsch = int(h/2)
		cv2.rectangle(frame, (hscw, hsch), (hscw, hsch), (0, 0, 255), 4)
		
		#calculate position and send to arduino
		idkx = (w/2)-centerx
		idky = (h/2)-centery
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
		ser.readline()
		

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
