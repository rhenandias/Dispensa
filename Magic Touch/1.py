import imutils
import cv2
import matplotlib.pyplot as plt
import time 
import numpy as np

# Carrega imagens
image = cv2.imread("printscreen.jpeg")
pattern1 = cv2.imread("pattern1.jpg")
pattern2 = cv2.imread("pattern2.jpg")	

(image_h, image_w, image_d) = image.shape
(pattern1_h, pattern1_w, pattern1_d) = pattern1.shape
resized = imutils.resize(image, width = int(image_w / 2))
resized_pattern1 = imutils.resize(pattern1, width = int(pattern1_w / 2))

(h, w, d) = resized_pattern1.shape

start = time.clock()
img = resized.copy()

# Apply template Matching
res = cv2.matchTemplate(img,resized_pattern1, cv2.TM_CCOEFF)
end = time.clock()

print(str(end-start) + " for " + "cv2.TM_CCOEFF") 

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(img,top_left, bottom_right, 255, 2)

plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle("cv2.TM_CCOEFF")

plt.show()

img_rgb = resized.copy()
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

template = resized_pattern1.copy()
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

(h, w) = template_gray.shape

res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.5
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imshow('res.png',img_rgb)
cv2.waitKey(0)

