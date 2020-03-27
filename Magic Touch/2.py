import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np

image_resize_ratio = 2
pattern_resize_ratio = 2

# Carrega imagens
image = cv2.imread("image1.jpg")
image = cv2.imread("image2.jpg")
image = cv2.imread("image3.jpg")
image = cv2.imread("image4.jpg")
pattern1 = cv2.imread("pattern1.png")
pattern2 = cv2.imread("pattern2.png")	
pattern3 = cv2.imread("pattern3.png")	
pattern4 = cv2.imread("pattern4.png")	

# Cria lista com patterns
patterns = [pattern1, pattern2, pattern3, pattern4]

pattern_colors = [(205, 0,0), (105,30, 210), (250,154, 0), (255, 0, 255)]

# Redimensiona imagem base
(image_h, image_w, image_d) = image.shape
resized_image = imutils.resize(image, width = int(image_w / image_resize_ratio))

# Redimensiona patterns
resized_patterns = []
for pattern in patterns:
	(pattern_h, pattern_w, pattern_d) = pattern.shape
	resized_pattern = imutils.resize(pattern, width = int(pattern_w / pattern_resize_ratio))
	resized_patterns.append(resized_pattern)

for idx, pattern in  enumerate(resized_patterns):	
	img_rgb = resized_image.copy()

	template = pattern.copy()

	(h, w, d) = template.shape

	res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.7
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), pattern_colors[idx], 2)

	cv2.imshow('res.png',img_rgb)
	cv2.waitKey(0)

