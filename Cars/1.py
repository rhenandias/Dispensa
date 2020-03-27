import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np
import pyautogui
import math

offset = [0, -28]					# Offset para posicionamento do recorte de tela após identificar o header do jogo
window_size = [1190, 670]			# Tamanho do recorte da tela do jogo

# Identifica posição do header do jogo na tela do computador
header_position = pyautogui.locateOnScreen("header.png", confidence=0.5)
coord = (header_position[0] - offset[0], header_position[1] - offset[1])

# Trained XML classifiers describes some features of some object we want to detect 
car_cascade = cv2.CascadeClassifier('cars.xml') 

# Game Loop
while True:
	game_screen = pyautogui.screenshot(region=(coord[0], coord[1], window_size[0], window_size[1]))
	game_screen = np.array(game_screen)[:, :, ::-1].copy()

	game_screen = imutils.resize(game_screen, width=700)

	# convert to gray scale of each frames 
	gray = cv2.cvtColor(game_screen, cv2.COLOR_BGR2GRAY) 
      
    # Detects cars of different sizes in the input image 
	cars = car_cascade.detectMultiScale(gray, 1.1, 10) 
      
    # To draw a rectangle in each cars 
	for (x,y,w,h) in cars: 
		cv2.rectangle(game_screen,(x,y),(x+w,y+h),(0,0,255),2) 
  
   	# Display frames in a window  
	cv2.imshow("game", game_screen)
	cv2.waitKey(1)
