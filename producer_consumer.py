"""
Producer/Consumer.

This script is made as an example of implementation and usage
of producer/consumer synchronization problem.

It requires "fei.ppds", "time", "random" and "matplotlib" imports.
"""
from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint
import matplotlib.pyplot as plt


class Shared(object):
    """
    Shared class shared between threads.

    Attributes
    ----------
    n: number of threads\n
    finished: boolean value if the execution has finished\n
    mutex: Mutex class used to lock/unlock\n
    free: Semaphore class representing how much free space is left\n
    items: Semaphore class representing number of items\n
    current_load: sum of currently stored items in a warehouse
    """
    def __init__(self, n):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(n)
        self.items = Semaphore(0)
        self.current_load = 0


def producer(shared, buffer):
    """
    Function representing producer adding items to warehouse

    Parameters
    ----------
    shared: shared sync object (Shared)\n
    buffer: buffer used for saving experimental data

    Return value
    ------------
    None

    :param shared: shared sync object -> Shared
    :param buffer: buffer used for saving experimental data
    """
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
        sleep(randint(1, 10)/10)
        # leave the warehouse
        shared.mutex.unlock()
        # increase items in warehouse
        shared.items.signal()


def consumer(shared, buffer):
    """
    Function representing consumer picking items from warehouse

    Parameters
    ----------
    shared: shared sync object (Shared)\n
    buffer: buffer used for saving experimental data

    Return value
    ------------
    None

    :param shared: shared sync object -> Shared
    :param buffer: buffer used for saving experimental data
    """
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
        sleep(randint(1, 10)/10)
        # leave warehouse
        shared.mutex.unlock()
        # process the item picked from warehouse
        sleep(randint(1, 10)/10)


def main():
    """
    Main function used for execution of code.

    :return: None
    """
    for i in range(10):
        buffer = []
        s = Shared(10)

        c = [Thread(consumer, s, buffer) for _ in range(20)]
        p = [Thread(producer, s, buffer) for _ in range(5)]

        sleep(5)
        s.finished = True
        print("Thread waits")
        s.items.signal(100)
        s.free.signal(100)
        [t.join() for t in c+p]
        print("Thread finished")
        print(buffer)

        plt.hist(buffer, bins=25)
        plt.ylabel("Warehouse fulfillment at each point of execution")
        plt.xlabel(f"20 consumers, 5 producers - run {i}")
        plt.show()


if __name__ == "__main__":
    main()
