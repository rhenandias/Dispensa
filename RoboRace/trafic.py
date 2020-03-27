# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import imutils
import time
import cv2
import numpy as np
import math

def adapt(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def euclidian_distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

red_sample_image = cv2.imread('red.png')
green_sample_image = cv2.imread('green.png')
color_red = cv2.imread('color_red.png')

def dominant_color(img):
    data = np.reshape(img, (-1,3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

    return(centers[0].astype(np.int32))

def trafic_light(img, title, bgr_target, threshold):
	start = time.perf_counter()
	# Isolamento da cor especificada
	img_bgr = img.copy()
	blurred = cv2.GaussianBlur(img_bgr, (11, 11), 0)
	img_hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	hsv_target = cv2.cvtColor(np.uint8([[bgr_target]]), cv2.COLOR_BGR2HSV)

	min_hsv = np.uint16([[[hsv_target[0][0][0] - threshold, 100, 100]]])
	max_hsv = np.uint16([[[hsv_target[0][0][0] + threshold, 255, 255]]])
	mask_hsv = cv2.inRange(img_hsv, min_hsv, max_hsv)

	mask_hsv = cv2.erode(mask_hsv, None, iterations=2)
	mask_hsv = cv2.dilate(mask_hsv, None, iterations=2)

	# result = cv2.bitwise_and(img_bgr, img_bgr, mask = mask_hsv)

	# Detecção de circulo
	cnts = cv2.findContours(mask_hsv.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(cnts)

	centers = []
	for c in contours:
		(x,y),r = cv2.minEnclosingCircle(c)
		r = int(r)
		center = (int(x),int(y), r)
		if r >= 3 and r<=12:
			centers.append(center)

	margin = 80
	for current_center in centers:
		for target_center in centers:
			distance = euclidian_distance(current_center[0], current_center[1], target_center[0], target_center[1])
			if distance <= margin and current_center != target_center:
				centers.remove(target_center)

	for center in centers:
		r = center[2] + 5
		color = (0, 255, 0) if title == 'green' else (0, 0, 255)
		cv2.circle(img_bgr, (center[0], center[1]), r, color, 2)

	end = time.perf_counter()
	print('elapsed', end - start)
	return img_bgr

red_detection = trafic_light(red_sample_image, 'red', [61, 3, 216], 40)
green_detection = trafic_light(green_sample_image, 'green', [210, 253,  45], 10)


result = cv2.bitwise_and(frame, red_detection)
result = cv2.bitwise_and(frame, result)

cv2.imshow('red', red_detection)
cv2.imshow('green', green_detection)
cv2.imshow('result', result)

cv2.waitKey(0)