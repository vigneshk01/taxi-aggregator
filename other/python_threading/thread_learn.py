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

#-------------------------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(thread_function, range(3))

#-----------------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------------------------------------

def producer(pipeline, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")

    logging.info("Producer received EXIT event. Exiting")


def consumer(pipeline, event):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info(
            "Consumer storing message: %s  (queue size=%s)",
            message, pipeline.qsize(),
        )

    logging.info("Consumer received EXIT event. Exiting")


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    def set_message(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()

#-------------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------