import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np
import pyautogui


image_resize_ratio = 1

offset = [0, -28]
window_size = [375, 660]

coord = pyautogui.locateOnScreen("header.png", confidence=0.9)

while True:
	# start = time.clock()
	screen = pyautogui.screenshot(region=(coord[0] - offset[0], coord[1] - offset[1], window_size[0], window_size[1]))
	open_cv_image = np.array(screen) 
	open_cv_image = open_cv_image[:, :, ::-1].copy()
	(image_h, image_w, image_d) = open_cv_image.shape
	resized_image = imutils.resize(open_cv_image, width = int(image_w / image_resize_ratio))
	# end = time.clock()
	# print(end - start)
	cv2.imshow("game", resized_image)
	cv2.waitKey(5)



cv2.imshow("", resized_image)
cv2.waitKey(0)
