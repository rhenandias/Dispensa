import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np
import pyautogui
import math

image_resize_ratio = 1
pattern_resize_ratio = 1

font = cv2.FONT_HERSHEY_SIMPLEX

pattern1 = cv2.imread("pattern11.png")
pattern2 = cv2.imread("pattern22.png")	
pattern3 = cv2.imread("pattern33.png")	
pattern4 = cv2.imread("pattern44.png")	

# Cria lista com patterns e imagens
patterns = [pattern1, pattern2, pattern3, pattern4]

# Lista de cores para os patterns
pattern_colors = [(205, 0,0), (105,30, 210), (250,154, 0), (255, 0, 255)]

# Redimensiona patterns
resized_patterns = []
for pattern in patterns:
	(pattern_h, pattern_w, pattern_d) = pattern.shape
	resized_pattern = imutils.resize(pattern, width = int(pattern_w / pattern_resize_ratio))
	resized_patterns.append(resized_pattern)

offset = [0, -28]
window_size = [375, 660]

coord = pyautogui.locateOnScreen("header.png", confidence=0.9)

while True:
	game_screen = pyautogui.screenshot(region=(coord[0] - offset[0], coord[1] - offset[1], window_size[0], window_size[1]))
	game_screen = np.array(game_screen)[:, :, ::-1].copy()

	img_rgb = game_screen.copy()
	cv2.imwrite('last_screen.png', game_screen)

	total_points = 0

	for idx, pattern in  enumerate(resized_patterns):	

		template = pattern.copy()

		(h, w, d) = template.shape

		res = cv2.matchTemplate(game_screen, template, cv2.TM_CCOEFF_NORMED )
		threshold = 0.6
		loc = np.where( res >= threshold)

		points = list(zip(*loc[::-1]))

		margin = 10

		for current_point in points:
			for target_point in points:
				distance = math.sqrt((target_point[0] - current_point[0])**2 + (target_point[1] - current_point[1])**2)
				if distance <= margin and distance > 0 and target_point in points: 
					points.remove(target_point)

		total_points = total_points + len(points)

		for pt in points:
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), pattern_colors[idx], 2)

	cv2.putText(img_rgb,str(total_points),(10,60), font,2,(0,0,255),2,cv2.LINE_AA)
	cv2.imshow("game", img_rgb)
	cv2.waitKey(1)

