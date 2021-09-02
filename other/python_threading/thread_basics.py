# import logging
# import threading
# import time
#
#
# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     logging.info("Main    : before creating thread")
#     x = threading.Thread(target=thread_function, args=(1,), daemon=True)
#     logging.info("Main    : before running thread")
#     x.start()
#     logging.info("Main    : wait for the thread to finish")
#     x.join()
#     logging.info("Main    : all done")

# -------------------------------------------------------------------------------------------------------------
import concurrent.futures
import logging
import queue
import threading
import time

# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     threads = list()
#     for index in range(3):
#         logging.info("Main    : create and start thread %d.", index)
#         x = threading.Thread(target=thread_function, args=(index,))
#         threads.append(x)
#         x.start()
#
#     for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)

# ----------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(thread_function, range(3))

# -----------------------------------------------------------------------------------------------------------

# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#
#     def update(self, name):
#         logging.info("Thread %s: starting update", name)
#         local_copy = self.value
#         local_copy += 1
#         time.sleep(0.1)
#         self.value = local_copy
#         logging.info("Thread %s: finishing update", name)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(2):
#             executor.submit(database.update, index)
#     logging.info("Testing update. Ending value is %d.", database.value)

# ----------------------------------------------------------------------------------------------------------

# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#         self._lock = threading.Lock()
#
#     def locked_update(self, name):
#         logging.info("Thread %s: starting update", name)
#         logging.debug("Thread %s about to lock", name)
#         with self._lock:
#             logging.debug("Thread %s has lock", name)
#             local_copy = self.value
#             local_copy += 1
#             time.sleep(0.1)
#             self.value = local_copy
#             logging.debug("Thread %s about to release lock", name)
#         logging.debug("Thread %s after release", name)
#         logging.info("Thread %s: finishing update", name)
#
#
# if __name__ == "__main__":
#
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)
#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(2):
#             executor.submit(database.locked_update, index)
#     logging.info("Testing update. Ending value is %d.", database.value)

# --------------------------------------------------------------------------------------------------------

import random

SENTINEL = object()

# def producer(pipeline):
#     """Pretend we're getting a message from the network."""
#     for index in range(2):
#         message = random.randint(1, 101)
#         # time.sleep(10)
#         logging.info("Producer got message: %s", message)
#         pipeline.set_message(message, "Producer")
#
#     # Send a sentinel message to tell consumer we're done
#     pipeline.set_message(SENTINEL, "Producer")
#
#
# def consumer(pipeline):
#     """Pretend we're saving a number in the database."""
#     message = 0
#     while message is not SENTINEL:
#         message = pipeline.get_message("Consumer")
#         if message is not SENTINEL:
#             logging.info("Consumer storing message: %s", message)
#
#
# class Pipeline:
#     """
#     Class to allow a single element pipeline between producer and consumer.
#     """
#
#     def __init__(self):
#         self.message = 0
#         self.producer_lock = threading.Lock()
#         self.consumer_lock = threading.Lock()
#         self.consumer_lock.acquire()
#
#     def get_message(self, name):
#         logging.debug("%s:about to acquire getlock", name)
#         time.sleep(10)
#         self.consumer_lock.acquire()
#         logging.debug("%s:have getlock", name)` A
#         message = self.message
#         logging.debug("%s:about to release setlock", name)
#         self.producer_lock.release()
#         logging.debug("%s:setlock released", name)
#         return message
#
#     def set_message(self, message, name):
#         logging.debug("%s:about to acquire setlock", name)
#         self.producer_lock.acquire()
#         logging.debug("%s:have setlock", name)
#         self.message = message
#         logging.debug("%s:about to release getlock", name)
#         self.consumer_lock.release()
#         logging.debug("%s:getlock released", name)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)
#
#     pipeline = Pipeline()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline)
#         executor.submit(consumer, pipeline)

# ------------------------------------------------------------------------------------------------------------

# def producer(pipeline, event):
#     """Pretend we're getting a number from the network."""
#     while not event.is_set():
#         message = random.randint(1, 101)
#         logging.info("Producer got message: %s", message)
#         pipeline.set_message(message, "Producer")
#
#     logging.info("Producer received EXIT event. Exiting")
#
#
# def consumer(pipeline, event):
#     """Pretend we're saving a number in the database."""
#     while not event.is_set() or not pipeline.empty():
#         message = pipeline.get_message("Consumer")
#         logging.info(
#             "Consumer storing message: %s  (queue size=%s)",
#             message, pipeline.qsize(),
#         )
#
#     logging.info("Consumer received EXIT event. Exiting")
#
#
# class Pipeline(queue.Queue):
#     def __init__(self):
#         super().__init__(maxsize=10)
#
#     def get_message(self, name):
#         logging.debug("%s:about to get from queue", name)
#         value = self.get()
#         logging.debug("%s:got %d from queue", name, value)
#         return value
#
#     def set_message(self, value, name):
#         logging.debug("%s:about to add %d to queue", name, value)
#         self.put(value)
#         logging.debug("%s:added %d to queue", name, value)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)
#
#     pipeline = Pipeline()
#     event = threading.Event()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline, event)
#         executor.submit(consumer, pipeline, event)
#
#         time.sleep(0.1)
#         logging.info("Main: about to set event")
#         event.set()

# -------------------------------------------------------------------------------------------------------

# import concurrent.futures
# import logging
# import queue
# import random
# import threading
# import time
#
# def producer(queue, event):
#     """Pretend we're getting a number from the network."""
#     while not event.is_set():
#         message = random.randint(1, 101)
#         logging.info("Producer got message: %s", message)
#         queue.put(message)
#
#     logging.info("Producer received event. Exiting")
#
# def consumer(queue, event):
#     """Pretend we're saving a number in the database."""
#     while not event.is_set() or not queue.empty():
#         message = queue.get()
#         logging.info(
#             "Consumer storing message: %s (size=%d)", message, queue.qsize()
#         )
#
#     logging.info("Consumer received event. Exiting")
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     pipeline = queue.Queue(maxsize=10)
#     event = threading.Event()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline, event)
#         executor.submit(consumer, pipeline, event)
#
#         time.sleep(0.1)
#         logging.info("Main: about to set event")
#         event.set()

# ----------------------------------------------------------------------------------------------------

# import queue
# import random
# from datetime import datetime, timedelta
# from threading import Thread
# import requests
#
# BASE_URL = "http://localhost:5000"
# resp = requests.get(f"{BASE_URL}/exchanges")
# EXCHANGES = resp.json()
# START_DATE = datetime(2020, 3, 1)
# DATES = [(START_DATE + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)]
# resp = requests.get(f"{BASE_URL}/symbols")
# SYMBOLS = resp.json()
# len(EXCHANGES) * len(SYMBOLS) * len(DATES)
#
#
# def check_price(exchange, symbol, date, base_url=BASE_URL):
#     resp = requests.get(f"{base_url}/price/{exchange}/{symbol}/{date}")
#     return resp.json()
#
#
# exchange, symbol, date = random.choice(EXCHANGES), random.choice(SYMBOLS), random.choice(DATES)
# check_price(exchange, symbol, date)
#
# tasks = queue.Queue()
# for exchange in EXCHANGES:
#     for date in DATES:
#         for symbol in SYMBOLS:
#             task = {
#                 'exchange': exchange,
#                 'symbol': symbol,
#                 'date': date,
#             }
#             tasks.put(task)
#
# tasks.qsize()
#
#
# class PriceResults:
#     def __init__(self):
#         results = {}
#         for exchange in EXCHANGES:
#             results[exchange] = {}
#             for date in DATES:
#                 results[exchange][date] = {}
#                 for symbol in SYMBOLS:
#                     results[exchange][date][symbol] = None
#         self._results = results
#
#     def put_price(self, price, exchange, symbol, date):
#         self._results[exchange][date][symbol] = price
#
#     def get_price(self, exchange, symbol, date):
#         return self._results[exchange][date][symbol]
#
#
# def worker(task_queue, results):
#     while True:
#         try:
#             task = task_queue.get(block=False)
#         except queue.Empty:
#             print('Queue is empty! My work here is done. Exiting.')
#             return
#         exchange, symbol, date = task['exchange'], task['symbol'], task['date']
#         price = check_price(exchange, symbol, date)
#         results.put_price(price, exchange, symbol, date)
#         task_queue.task_done()
#
#
# results = PriceResults()
# MAX_WORKERS = 32
# threads = [Thread(target=worker, args=(tasks, results)) for _ in range(MAX_WORKERS)]
# [t.start() for t in threads]
# tasks.join()
# tasks.qsize()
# any([t.is_alive() for t in threads])
#
# for _ in range(5):
#     exchange, symbol, date = random.choice(EXCHANGES), random.choice(SYMBOLS), random.choice(DATES)
#     price = results.get_price(exchange, symbol, date)
#     if price:
#         print(f"{exchange.title():<20} price of {symbol.upper():^5} on {date:^10} was: ${round(price['close'], 4):>9}")
#     else:
#         print(f"No price of {symbol.upper()} for {exchange.title()} on {date}")

# ----------------------------------------------------------------------------

# import threading
# import time
# import os
#
#
# def main():
#     print("Python Process and Threading Example")
#     print("-" * 40)
#     main_pid = (format(os.getpid()))
#     main_name = (format(threading.main_thread().name))
#     main_count = (format(threading.active_count()))
#     print(f"Main Porgram Process ID (PID): {main_pid}")
#     print(f"Main Thread Name: {main_name}")
#     print(f"Total of Currently Live Threading Objects: {main_count}")
#
#     threads()
#
#
# def threads():
#     thread1 = threading.Thread(target=task1, name='thread1')
#
#     thread2 = threading.Thread(target=task2, name='thread2')
#     time.sleep(2)
#
#     thread1.start()
#     thread2.start()
#     time.sleep(2)
#
#     thread1.join()
#     thread2.join()
#     time.sleep(2)
#
#
# def task1():
#     tid1 = (format(threading.current_thread().name))
#     pid1 = (format(os.getpid()))
#     print(f"nTask 1 - Thread ID (TID): {tid1}")
#     print(f"Task 1 - Process ID (PID): {pid1}")
#
#
# def task2():
#     tid2 = (format(threading.current_thread().name))
#     pid2 = (format(os.getpid()))
#     print(f"nTask 2 - Thread ID (TID): {tid2}")
#     print(f"nTask 2 - Process ID (PID): {pid2}")
#
#
# if __name__ == "__main__":
#     main()
