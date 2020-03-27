import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np
import pyautogui
import math

font = cv2.FONT_HERSHEY_SIMPLEX
offset = [0, -28]
window_size = [375, 660]
mouse_speed = 0.2

pattern1 = cv2.imread("pattern11.png")
pattern2 = cv2.imread("pattern22.png")	
pattern3 = cv2.imread("pattern33.png")	
pattern4 = cv2.imread("pattern44.png")	

# Cria lista com patterns
patterns = [pattern1, pattern2, pattern3, pattern4]

# Lista de cores para os patterns
pattern_colors = [(205, 0,0), (105,30, 210), (250,154, 0), (255, 0, 255)]

header_position = pyautogui.locateOnScreen("header.png", confidence=0.5)
coord = (header_position[0] - offset[0], header_position[1] - offset[1])

pattern_profiles = {
	'0' : [(152,533),(193,462),(234,533)],
	'1' : [(152,462),(193,533),(234,462)],
	'2' : [(152,497),(234,497)],
	'3' : [(193,533),(193,462)]
}

def run_pattern_profile(profile_id):
	# Adquire o padrão que vai ser executado
	cur_pattern = pattern_profiles[profile_id]
	# Clica com o mouse no primeiro ponto do padrão
	pyautogui.mouseDown(button='left', x =coord[0] + cur_pattern[0][0], y = coord[1] + cur_pattern[0][1])
	# Percorre os pontos seguintes com o mouse pressionado
	for i in range(1, len(cur_pattern)):
		pyautogui.moveTo(x = coord[0] + cur_pattern[i][0], y = coord[1] + cur_pattern[i][1], duration=mouse_speed)
	# Após o último ponto do padrão, solta o botão do mouse
	pyautogui.mouseUp(button='left')
 
executed_profiles = 0
while True:
	game_screen = pyautogui.screenshot(region=(coord[0], coord[1], window_size[0], window_size[1]))
	game_screen = np.array(game_screen)[:, :, ::-1].copy()

	img_rgb = game_screen.copy()
	cv2.imwrite('last_screen.png', game_screen)

	total_points = 0

	active_profiles = []

	for idx, pattern in  enumerate(patterns):	

		template = pattern.copy()

		(h, w, d) = template.shape

		res = cv2.matchTemplate(game_screen, template, cv2.TM_CCOEFF_NORMED )
		threshold = 0.65
		loc = np.where( res >= threshold)

		points = list(zip(*loc[::-1]))

		margin = 5

		for current_point in points:
			for target_point in points:
				distance = math.sqrt((target_point[0] - current_point[0])**2 + (target_point[1] - current_point[1])**2)
				if distance <= margin:
					points.remove(target_point)

		total_points = total_points + len(points)

		if len(points): active_profiles.append(idx)

		for pt in points:
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), pattern_colors[idx], 2)

	cv2.putText(img_rgb,'Active profiles: ' + str(total_points),(10,500), font,1,(0,0,255),2,cv2.LINE_AA)
	cv2.putText(img_rgb,'Executed profiles: ' + str(executed_profiles),(10,540), font,1,(255,0,0),2,cv2.LINE_AA)
	cv2.imshow("game", img_rgb)
	cv2.waitKey(1)

	for profile in active_profiles:
		run_pattern_profile(str(profile))
		active_profiles = [i for i in active_profiles if i != profile]
		time.sleep(0.2)
		executed_profiles = executed_profiles + 1

