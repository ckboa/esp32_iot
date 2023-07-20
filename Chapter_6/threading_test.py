import _thread
from time import *

def time_test(task_id):
    print("Start task {} at : {}".format(task_id, ticks_ms()))
    sleep(2)
    print("End task {} at : {}".format(task_id, ticks_ms()))


time_start = ticks_ms()
print("Start task at : ", time_start) 
_thread.start_new_thread(time_test, (1,))
_thread.start_new_thread(time_test, (2,))
time_end = ticks_ms()

print("End task at : ", time_start) 
print("total time spend : ", time_end - time_start )
_thread.exit()