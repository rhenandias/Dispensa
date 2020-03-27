# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import imutils
import time
import cv2
import numpy as np
import math

vs = cv2.VideoCapture("free.mp4")

# Função para calcular distância entre dois pontos
def euclidian_distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

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

	# Detecção de circulo
	contours = cv2.findContours(mask_hsv.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)

	# Detecta circulos
	centers = []
	for c in contours:
		(x,y),r = cv2.minEnclosingCircle(c)
		r = int(r)
		center = (int(x),int(y), r)
		if r >= 3 and r<=12:
			centers.append(center)

	# Filtro
	margin = 80
	for current_center in centers:
		for target_center in centers:
			distance = euclidian_distance(current_center[0], current_center[1], target_center[0], target_center[1])
			if distance <= margin and current_center != target_center:
				centers.remove(target_center)

	# Desenha contornos
	for center in centers:
		r = center[2] + 5
		color = (0, 255, 0) if title == 'green' else (0, 0, 255)
		cv2.circle(img_bgr,(center[0], center[1]),r,color,2)

	end = time.perf_counter()
	# print('elapsed', end - start)
	return img_bgr

frame_counter = 0
# loop over the frames of the video
while True:
	# Frame é adquirido aqui
	response, frame = vs.read()

	if frame is None:
		break

	# Modificações no frame são feitas aqui
	red_detection = trafic_light(frame, 'red'  , [61 ,   3, 216], 20)
	green_detection = trafic_light(frame, 'green', [210, 253,  45], 10)

	frame = cv2.bitwise_or(frame, red_detection)
	frame = cv2.bitwise_or(frame, green_detection)
	# Exibição dos resultados
	cv2.imshow("video", frame)
	cv2.imshow('red', red_detection)
	cv2.imshow('green', green_detection)
	cv2.waitKey(1)

	frame_counter = frame_counter + 1
	print('frame', frame_counter)