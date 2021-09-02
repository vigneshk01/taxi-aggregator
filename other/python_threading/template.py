import logging
import os
import time
from concurrent.futures import ProcessPoolExecutor

# list of taxi's to process
arr = ['taxi_1', 'taxi_2']


class MyProject:
    def __init__(self, tid):
        self._result = ''
        self._start_time = time.time()
        self._tid = tid
        self.base_fun()

    def __repr__(self):
        return str(self._result)

    def process_stat(self):
        end_time = time.time()
        time_diff = end_time - self._start_time
        print("child_id: %s start_time: %s, end time: %s, total_time: %s " % (
            get_pid(), self._start_time, end_time, time_diff), flush=True)

    def fun_one(self):
        pid = get_pid()
        self._result = self._tid
        # logging.debug(self._result)
        logging.debug(f" (PID): {pid} - f1 - {self._result}")
        print(f" (PID): {pid} - f1 - {self._result}", flush=True)

    def fun_two(self):
        pid = get_pid()
        self._result = self._tid
        # logging.debug(self._result)
        logging.debug(f" (PID): {pid} - f2 - {self._result}")
        print(f" (PID): {pid} - f2 - {self._result}", flush=True)

    def base_fun(self):
        # --------------  placeholder for the functions -------------------------------
        # while 1 == 1:
        self.fun_one()
        # time.sleep(1)
        self.fun_two()
        # time.sleep(1)
        self.process_stat()


def get_pid():
    pid = (format(os.getpid()))
    return pid


def worker(tid):
    log_filename = './basic_file.log'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename=log_filename)
    pjt = MyProject(tid)
    return pjt


if __name__ == "__main__":

    start = time.time()

    with ProcessPoolExecutor(2) as p:
        results = p.map(worker, arr)

    # for res in results:
    #     print(res)

    end = time.time()
    diff = end - start

    print("parent_id: %s, start_time: %s , end time: %s, total_time: %s" % (get_pid(), start, end, diff))
