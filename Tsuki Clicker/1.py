import time, os

# 1788

clicks = 0
while True:
	os.popen("adb shell input touchscreen tap 150 150")
	clicks = clicks + 1
	print("Clicando ... " + str(clicks))
	time.sleep(0.2)
