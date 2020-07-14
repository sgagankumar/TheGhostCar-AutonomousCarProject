#!/usr/bin/env python

"""TrafficLight.py: Recognises and Classifies Light, by identifying Red Culoured Light Sources."""

__author__ = "S.GAGAN KUMAR"
__project__ = "The Ghost Car: Autonomous Car Project"
__link__ = "www.github.com/sgagankumar"
__date__ = "12-Jul-2020"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "sgagankumar@gmail.com"
__status__ = "Completed", "Tested"

# importing the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

print("Started")

#Video Source Initialisation - (Replace with 0 for default device camera)
cap = cv2.VideoCapture('detections.mp4')

while(cap.isOpened()):
	_, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)						#Coverting to GrayScale
	blurred = cv2.GaussianBlur(gray, (11, 11), 0)						#Applying 11x11 Blur
	thresh = cv2.threshold(blurred, 245, 255, cv2.THRESH_BINARY)[1]		#Masking only Red Light Sources

	cv2.imshow('Display - Actual View', frame)
	cv2.imshow('Display - Light Sources', thresh)

	for row in range(len(thresh)):
		if 255 in thresh[row]:
			for col in range(len(thresh[0])):
				if 255 == thresh[row][col]:
					# print(row,',',col)
					coordinate=[(col-20,row-20),(col+20,row+70)]
					#Displaying a Rectangle marking light Source
					cv2.rectangle(frame,coordinate[0],coordinate[1], (0, 255, 0), 2)
					break
	cv2.imshow('Display - With Traffic Light Detection', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()