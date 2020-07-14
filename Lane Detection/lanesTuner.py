import cv2
import numpy as np
import matplotlib.pyplot as plt

imageLocation = 'test_image.jpg'
threshold = 100


def canny(image):
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	canny=cv2.Canny(blur, 50, 150)
	return canny


def display_lines(image, lines):
	line_image = np.zeros_like(image)
	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line.reshape(4)
			cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
	return line_image


def region_of_interest(image):
	height = image.shape[0]
	width = image.shape[0]
	polygons = np.array([[(200, height), (1100, height), (550,250)]])
	mask = np.zeros_like(image)
	cv2.fillPoly(mask, polygons, 255)
	masked_image = cv2.bitwise_and(image, mask)
	return masked_image


image = cv2.imread(imageLocation)
lane_image = np.copy(image)
canny = canny(lane_image)
roi = region_of_interest(canny)
lines = cv2.HoughLinesP(roi, 2, np.pi/180, threshold, np.array([]), minLineLength=40, maxLineGap=5)
line_image = display_lines(lane_image, lines)
overlay = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

cv2.imshow('Overlay', overlay)
cv2.waitKey(0)