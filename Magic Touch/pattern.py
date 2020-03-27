import imutils
import cv2
import time 
import numpy as np
import pyautogui
import math

offset = [0, -28]
window_size = [375, 660]

header_position = pyautogui.locateOnScreen("header.png", confidence=0.9)
coord = (header_position[0] - offset[0], header_position[1] - offset[1])

pattern_profiles = {
	'0' : [(152,533),(193,462),(234,533)],
	'1' : [(152,462),(193,533),(234,462)],
	'2' : [(152,497),(234,497)],
	'3' : [(193,533),(193,462)],
	'4' : [(179,451),(216,499),(193,522),(170,499),(207,451)]
}

def run_pattern_profile(profile_id):
	# Adquire o padrão que vai ser executado
	cur_pattern = pattern_profiles[profile_id]
	# Clica com o mouse no primeiro ponto do padrão
	pyautogui.mouseDown(button='left', x =coord[0] + cur_pattern[0][0], y = coord[1] + cur_pattern[0][1])
	# Percorre os pontos seguintes com o mouse pressionado
	for i in range(1, len(cur_pattern)):
		pyautogui.moveTo(x = coord[0] + cur_pattern[i][0], y = coord[1] + cur_pattern[i][1])
	# Após o último ponto do padrão, solta o botão do mouse
	pyautogui.mouseUp(button='left')

run_pattern_profile(str(0))
run_pattern_profile(str(1))
run_pattern_profile(str(2))
run_pattern_profile(str(3))
run_pattern_profile(str(4))