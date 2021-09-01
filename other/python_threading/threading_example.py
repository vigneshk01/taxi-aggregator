import threading
import time
import os


def main():
    print("Python Process and Threading Example")
    print("-" * 40)
    main_pid = (format(os.getpid()))
    main_name = (format(threading.main_thread().name))
    main_count = (format(threading.active_count()))
    print(f"Main Porgram Process ID (PID): {main_pid}")
    print(f"Main Thread Name: {main_name}")
    print(f"Total of Currently Live Threading Objects: {main_count}")

    threads()


def threads():
    thread1 = threading.Thread(target=task1, name='thread1')

    thread2 = threading.Thread(target=task2, name='thread2')
    time.sleep(2)

    thread1.start()
    thread2.start()
    time.sleep(2)

    thread1.join()
    thread2.join()
    time.sleep(2)


def task1():
    tid1 = (format(threading.current_thread().name))
    pid1 = (format(os.getpid()))
    print(f"nTask 1 - Thread ID (TID): {tid1}")
    print(f"Task 1 - Process ID (PID): {pid1}")


def task2():
    tid2 = (format(threading.current_thread().name))
    pid2 = (format(os.getpid()))
    print(f"nTask 2 - Thread ID (TID): {tid2}")
    print(f"nTask 2 - Process ID (PID): {pid2}")


if __name__ == "__main__":
    main()
