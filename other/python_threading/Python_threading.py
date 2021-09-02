# import threading
#
#
# def print_cube(num):
#     for i in range(0, 10000000000000000000000000000000000000000000):
#         print(i)
#     print("cube:{}".format(num * num * num))
#
#
# def print_square(num):
#     for i in range(99999999999999999999999999999, 0, -9):
#         print(i)
#     print("square: {}".format(num * num))
#
#
# if __name__ == "__main__":
#     t1 = threading.Thread(target=print_square, args=(10,))
#     t2 = threading.Thread(target=print_cube, args=(10,))
#
#     t1.start()
#     t2.start()
#
#     # t1.join()
#     # t2.join()
#
#     print("Done!")

# --------------------------------------------------------------------------

# import threading
#
# # global variable x
# x = 0
#
#
# def increment():
#     # function to increment global variable x
#     global x
#     x += 1
#
#
# def thread_task():
#     # task for thread calls increment function 100000 times.
#     for _ in range(100000):
#         increment()
#
#
# def main_task():
#     global x
#     # setting global variable x as 0
#     x = 0
#
#     # creating threads
#     t1 = threading.Thread(target=thread_task)
#     t2 = threading.Thread(target=thread_task)
#
#     # start threads
#     t1.start()
#     t2.start()
#
#     # wait until threads finish their job
#     t1.join()
#     t2.join()
#
#
# if __name__ == "__main__":
#     for i in range(1):
#         main_task()
#         print("Iteration {0}: x = {1}".format(i, x))

# -------------------------------------------------------------------

# import threading
#
# # global variable x
# x = 0
#
#
# def increment():
#     # function to increment global variable x
#     global x
#     x += 1
#
#
# def thread_task():
#     # task for thread calls increment function 100000 times.
#     for _ in range(100000):
#         increment()
#
#
# def main_task():
#     global x
#     # setting global variable x as 0
#     x = 0
#
#     # creating threads
#     t1 = threading.Thread(target=thread_task)
#     t2 = threading.Thread(target=thread_task)
#
#     # start threads
#     t1.start()
#     t2.start()
#
#     # wait until threads finish their job
#     t1.join()
#     t2.join()
#
#
# if __name__ == "__main__":
#     for i in range(10):
#         main_task()
#         print("Iteration {0}: x = {1}".format(i, x))
