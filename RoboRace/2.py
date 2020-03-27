import time

# task_timeout = 3
# last_time = 0
# cur_time = 0
# while True:
# 	cur_time = time.perf_counter()
# 	if cur_time - last_time >= task_timeout:
# 		print(str(task_timeout) + ' s')
# 		last_time = time.perf_counter()


fps = 1
active_frame_time = 100/fps
print(active_frame_time)

task_timeout = 1
last_time = 0
cur_time = 0

while True:
	cur_time = time.perf_counter()
	time_elapsed_since_last_task = cur_time - last_time
	time_to_wait = None
	if time_elapsed_since_last_task < task_timeout:
		time_to_wait = task_timeout - time_elapsed_since_last_task
	else:
		time_to_wait = 0

	time.sleep(time_to_wait)
	
	print("Running Task")
	last_time = time.perf_counter()

	
	