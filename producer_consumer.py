from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint
import matplotlib.pyplot as plt


class Shared(object):
    def __init__(self, n):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(n)
        self.items = Semaphore(0)
        self.current_load = 0


def producer(shared, buffer):
    while True:
        sleep(randint(1, 10)/10)
        # check free space in the warehouse
        shared.free.wait()
        if shared.finished:
            break
        # get access to the warehouse
        shared.mutex.lock()
        # simulate load an item to the warehouse
        shared.current_load += 1
        buffer.append(shared.current_load)
        sleep(randint(1, 10)/100)
        # leave the warehouse
        shared.mutex.unlock()
        # increase items in warehouse
        shared.items.signal()


def consumer(shared, buffer):
    while True:
        # check warehouse resources
        shared.items.wait()
        if shared.finished:
            break
        # get access to the warehouse
        shared.mutex.lock()
        # simulate getting an item from the warehouse
        shared.current_load -= 1
        buffer.append(shared.current_load)
        sleep(randint(1, 10)/100)
        # leave warehouse
        shared.mutex.unlock()
        # process the item picked from warehouse
        sleep(randint(1, 10)/10)


def main():
    buffer = []
    s = Shared(10)
    c = [Thread(consumer, s, buffer) for _ in range(2)]
    p = [Thread(producer, s, buffer) for _ in range(10)]

    sleep(5)
    s.finished = True
    print("Thread waits")
    s.items.signal(100)
    s.free.signal(100)
    [t.join() for t in c+p]
    print("Thread finished")
    print(buffer)

    # plt.plot(buffer)
    # plt.ylabel('Current warehouse load')
    # plt.axes.get_xaxis().set_visible(False)
    # plt.show()


if __name__ == "__main__":
    main()
