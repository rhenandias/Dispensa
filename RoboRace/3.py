# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import imutils
import time
import cv2
import numpy as np
import math

vs = cv2.VideoCapture("junior.mp4")

# Função para calcular distância entre dois pontos
def euclidian_distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def trafic_light(img, title, bgr_target, threshold):
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

	result = cv2.bitwise_and(img_bgr, img_bgr, mask = mask_hsv)

	# Detecção de circulo
	contours = cv2.findContours(mask_hsv.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
	contours.sort(key=lambda x:cv2.boundingRect(x)[0])

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
		cv2.circle(img_bgr,(center[0], center[1]),r,(0,255,0),2)

	# cv2.imshow("preprocessed", img_bgr)

	# cv2.imshow("mask_hsv", mask_hsv)
	# cv2.imshow(title, result)
	# return result
	return img_bgr

# loop over the frames of the video
while True:
	# Frame é adquirido aqui
	response, frame = vs.read()

	if frame is None:
		break

	# Modificações no frame são feitas aqui
	red_detection = trafic_light(frame, 'red'  , [61 ,   3, 216], 20)
	green_detection = trafic_light(frame, 'green', [210, 253,  45], 10)

	# Exibição dos resultados
	cv2.imshow("video", frame)
	cv2.imshow('red', red_detection)
	cv2.imshow('green', green_detection)
	cv2.waitKey(1)