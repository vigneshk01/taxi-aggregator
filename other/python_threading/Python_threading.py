import threading


def print_cube(num):
    for i in range(0, 10000000000000000000000000000000000000000000):
        print(i)
    print("cube:{}".format(num * num * num))


def print_square(num):
    for i in range(99999999999999999999999999999, 0, -9):
        print(i)
    print("square: {}".format(num * num))


if __name__ == "__main__":
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))

    t1.start()
    t2.start()

    # t1.join()
    # t2.join()

    print("Done!")
