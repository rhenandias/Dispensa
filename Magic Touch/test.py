import cv2
import numpy as np
import os
import time

os.popen('adb shell "input touchscreen swipe 126 459 413 472 1000 & sleep 2 & input touchscreen swipe 413 472 72 776 1000 & sleep 1 & input touchscreen swipe 72 776 407 769 1000 & sleep 1 "')
