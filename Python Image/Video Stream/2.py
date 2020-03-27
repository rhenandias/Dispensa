import imutils
import cv2
import numpy as np 
import matplotlib.pyplot as plt

board = cv2.imread("board.png")
board = imutils.resize(board, width=500)
robot = cv2.imread("robot.png")

(h, w, d) = robot.shape

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

res = cv2.matchTemplate(board, robot, cv2.TM_CCOEFF)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(board, top_left, bottom_right, 255, 2)
cv2.imshow("Image", board)
cv2.waitKey(0)
