import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np
import math

image_resize_ratio = 2
pattern_resize_ratio = 2

# Carrega imagens
image1 = cv2.imread("image1.jpg")
image2 = cv2.imread("image2.jpg")
image3 = cv2.imread("image3.jpg")
image4 = cv2.imread("image4.jpg")

pattern1 = cv2.imread("pattern111.png")
pattern2 = cv2.imread("pattern222.png")	
pattern3 = cv2.imread("pattern333.png")	
pattern4 = cv2.imread("pattern444.png")	

# Cria lista com patterns e imagens
patterns = [pattern1, pattern2, pattern3, pattern4]
images = [image1, image2, image3, image4]

# Lista de cores para os patterns
pattern_colors = [(205,0,0), (105,30, 210), (250,154, 0), (255, 0, 255)]

print(pattern_colors)

# Redimensiona imagens
resized_images = []
for image in images:
	(image_h, image_w, image_d) = image.shape
	resized_image = imutils.resize(image, width = int(image_w / image_resize_ratio))
	resized_images.append(resized_image)

# Redimensiona patterns
resized_patterns = []
for pattern in patterns:
	(pattern_h, pattern_w, pattern_d) = pattern.shape
	resized_pattern = imutils.resize(pattern, width = int(pattern_w / pattern_resize_ratio))
	resized_patterns.append(resized_pattern)


for image in resized_images:
	img_rgb = image.copy()
	total_points = 0
	for idx, pattern in  enumerate(resized_patterns):	
		template = pattern.copy()

		(h, w, d) = template.shape

		res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
		threshold = 0.7
		loc = np.where( res >= threshold)
		points = list(zip(*loc[::-1]))

		print("\nPattern: " + str(idx))
		print("Antes do filtro: " + str(len(points)))

		margin = 20
	
		for current_point in points:
			for target_point in points:
				distance = math.sqrt((target_point[0] - current_point[0])**2 + (target_point[1] - current_point[1])**2)
				if distance <= margin and distance > 0 and target_point in points: 
					points.remove(target_point)

		print("Depois do filtro: " + str(len(points)))

		total_points = total_points + len(points)

		for pt in points:
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), pattern_colors[idx], 2)

	print("\nTotal points: " + str(total_points))
	cv2.imshow('res.png',img_rgb)
	cv2.waitKey(0)



# for image in resized_images:
# 	img_rgb = image.copy()
# 	for idx, pattern in  enumerate(resized_patterns):	
# 		template = pattern.copy()

# 		(h, w, d) = template.shape

# 		res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
# 		threshold = 0.7
# 		loc = np.where( res >= threshold)
# 		for pt in zip(*loc[::-1]):
# 			print(pt)
# 			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), pattern_colors[idx], 2)

# 	cv2.imshow('res.png',img_rgb)
# 	cv2.waitKey(0)

