#! /usr/bin/env python
# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
import rospy
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
from bottle import run, post, request, response
import threading
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def publishVision():

	# Initialize a ROS publisher noeuds
	#pub = rospy.Publisher('vision', String, queue_size=10)
	rospy.init_node('vision_objects', anonymous=True)
	velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	rate = rospy.Rate(10) # 10hz

	prototxt = "/home/lubuntu/Documents/robair_vision/catkin_ws/src/robair_opencv/scripts/MobileNetSSD_deploy.prototxt.txt"
	model = "/home/lubuntu/Documents/robair_vision/catkin_ws/src/robair_opencv/scripts/MobileNetSSD_deploy.caffemodel"
	confidence_total = 0.2

	# initialize the list of class labels MobileNet SSD was trained to
	# detect, then generate a set of bounding box colors for each class
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

	# load our serialized model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(prototxt, model)

	# initialize the video stream, allow the cammera sensor to warmup,
	# and initialize the FPS counter
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	fps = FPS().start()

	# loop over the frames from the video stream
	# while True:
	# We iterate while the ROS server is up
	while not rospy.is_shutdown():
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)


		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > confidence_total:
				# extract the index of the class label from the
				# `detections`, then compute the (x, y)-coordinates of
				# the bounding box for the object
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# draw the prediction on the frame
				label = "{}: {:.2f}%".format(CLASSES[idx],
					confidence * 100)
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

				rospy.loginfo(label)
				if CLASSES[idx] == "bottle" and confidence >= 0.7:
					vel_msg = Twist()
					vel_msg.linear.x = 2.0
					vel_msg.linear.y = 0
					vel_msg.linear.z = 0
					vel_msg.angular.x = 0
					vel_msg.angular.y = 0
					vel_msg.angular.z = 1.8
					velocity_publisher.publish(vel_msg)
				rate.sleep()

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

@post('/process')
def my_process():
	global move
	return str(move)

def server_thread():
	run(host='localhost', port=8080, debug=True)

if __name__ == "__main__":
	try:
		t = threading.Thread(target=server_thread)
		t.start()
		publishVision()
	except rospy.ROSInterruptException:
		pass
