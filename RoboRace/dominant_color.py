import cv2
import numpy as np

def dominant_color(img):
    data = np.reshape(img, (-1,3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

    return(centers[0].astype(np.int32))

img = cv2.imread('color_green.png')
print(dominant_color(img))