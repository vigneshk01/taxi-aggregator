import concurrent.futures
import os
import threading
import time

class Activities:
    def __init__(self):
        self.error = ''
        self._msg = ''
        # self._lock = threading.Lock()
        # self.call_funs()

    def fun_one(self):
        # with self._lock:
        self._msg = 'function_1'
        # time.sleep(5)
        print("the fun is %s" % self._msg)
        # return '\n' + self._msg

    def fun_two(self):
        # with self._lock:
        self._msg = 'function_2'
        # time.sleep(2)
        print("the fun is %s" % self._msg)
        # return '\n' + self._msg

    def fun_three(self):
        # with self._lock:
        self._msg = 'function_3'
        # time.sleep(4)
        print("the fun is %s" % self._msg)
        # return '\n' + self._msg

    def fun_four(self):
        # with self._lock:
        self._msg = 'function_4'
        # time.sleep(0.1)
        print("the fun is %s" % self._msg)
        # return '\n'  # + self._msg

    def fun_five(self):
        # with self._lock:
        self._msg = 'function_5'
        # time.sleep(1)
        print("the fun is %s" % self._msg)
        # return '\n' + self._msg

    def fun_six(self):
        # with self._lock:
        self._msg = 'function_6'
        # time.sleep(5)
        print("the fun is %s" % self._msg)
        # return '\n' + self._msg

    def fun_seven(self):
        # with self._lock:
        self._msg = 'function_7'
        # time.sleep(0.3)
        print("the fun is %s" % self._msg)
        # return '\n'  # +self._msg

    def call_funs(self, i=1):

        # while 1==1:
        print(f"[Process ID]:{os.getpid()} running..", flush=True)
        time.sleep(1)
        # return "done"


if __name__ == '__main__':
    start = time.time()
    print(start)
    with concurrent.futures.ProcessPoolExecutor(max_workers=7) as executors:
        processing = executors.map(Activities.call_funs, [x for x in range(1, 10)])
    for p in processing:
        print(p)

    end = time.time()
    diff = end - start
    print("time is %s" % diff)
