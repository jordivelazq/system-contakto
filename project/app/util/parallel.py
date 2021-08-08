from time import time

from concurrent.futures import ThreadPoolExecutor

def run_io_tasks_in_parallel(tasks):
	with ThreadPoolExecutor() as executor:
			running_tasks = [executor.submit(task) for task in tasks]
			for running_task in running_tasks:
					running_task.result()

# start = time()
# print_time(start, 1)
def print_time(start, prefix):
	end = time()
	print(str(prefix) + ': It took ' + str(end - start) + ' seconds!')
