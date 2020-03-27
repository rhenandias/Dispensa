from imutils.video import VideoStream
import numpy as numpy
import cv2
import imutils
import time

vs = VideoStream(src=1).start()
time.sleep(2)

while True:
	frame = vs.read()

	resized = imutils.resize(frame, width=400)
	ratio = resized.shape[0] / float(resized.shape[0])

	# blurred = cv2.GaussianBlur(resized, (11, 11), 0)
	
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

	edged = cv2.Canny(gray, 250, 250)

	thresh = cv2.threshold(edged, 250, 255, cv2.THRESH_BINARY_INV)[1]
	thresh = cv2.bitwise_not(thresh)

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	cnts = imutils.grab_contours(cnts)

	output = resized.copy()

	for c in cnts:
		# Calcula o centro do contorno
		M = cv2.moments(c)
		if M["m00"] != 0:
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.04 * peri, True)
			text = str(len(approx)) + " lados"
			cv2.drawContours(output, [c], -1, (0, 0, 255), 2)
			cv2.putText(output, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

	# cv2.drawContours(output, cnts, -1, (0, 0, 255), 2)

	cv2.imshow("Final", output)
	cv2.imshow("Edged", edged)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Raw", resized)
	key = cv2.waitKey(1) & 0xFF