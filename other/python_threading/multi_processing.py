import multiprocessing
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(200)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

# -------------------------------------------------------------------------

# importing the multiprocessing module
import multiprocessing


def print_cube(num):
    print("Cube: {}".format(num * num * num))


def print_square(num):
    print("Square: {}".format(num * num))


if __name__ == "__main__":
    # creating processes
    p1 = multiprocessing.Process(target=print_square, args=(10,))
    p2 = multiprocessing.Process(target=print_cube, args=(10,))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print("Done!")
# -------------------------------------------------------------------------

import concurrent
import concurrent.futures


class Calc:
    def __init__(self, a):
        self.a = a

    def calc(self, n):
        return self.a + n


class Process:
    def __init__(self):
        self.process_list = []
        self.executor = concurrent.futures.ProcessPoolExecutor(max_workers=4)
        # self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.calc = Calc(10)  # Instance of the class to process
        self.hoge = 3  # Instance variables

    def _process_bad(self, n):
        res = self.calc.calc(n) * self.hoge
        return res

    @staticmethod
    def _process(calc, n, hoge):
        res = calc.calc(n) * hoge
        return res

    def start_process(self, n):
        # Execution department
        # self.process_list.append(self.executor.submit(self._process_bad, n))  # NG
        self.process_list.append(self.executor.submit(self._process, self.calc, n, self.hoge))  # OK

    def get_result(self):
        # Get results
        self.executor.shutdown(wait=True)  # Shutdown before getting
        res_list = [res.result() for res in self.process_list]
        self.process_list = []
        return res_list


# abridgement

if __name__ == "__main__":
    process = Process()
    for i in range(10):
        process.start_process(i)
    result = process.get_result()
    print(result)
