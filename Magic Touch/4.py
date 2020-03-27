import subprocess
import cv2
import numpy as np
import imutils
import time

image_resize_ratio = 4

def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output

while True:
	start = time.clock()
	pipe = subprocess.Popen("adb shell screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
	image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
	(image_h, image_w, image_d) = image.shape
	resized_image = imutils.resize(image, width = int(image_w / image_resize_ratio))
	cv2.imshow("Window", resized_image)
	end = time.clock()
	print(end - start)