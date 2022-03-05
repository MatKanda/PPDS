"""
ADT LightSwitch.

This script is made as an example of implementation and usage
of lightswitch synchronization.

It requires "fei.ppds", "time" and "random" imports.
"""
from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class LightSwitch(object):
    """
    LightSwitch class shared between threads.

    Attributes
    ----------
    mutex: Mutex class used to lock/unlock
    counter: ounter for number of threads that reached certain point of execution
    """
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, room):
        self.mutex.lock()
        if not self.counter:
            room.wait()
        self.counter += 1
        self.mutex.unlock()

    def unlock(self, room):
        self.mutex.lock()
        self.counter -= 1
        if not self.counter:
            room.signal()
        self.mutex.unlock()


def reader(light_switch, room, turnstile):
    """
    Function representing reader reading some shared document

    Parameters
    ----------
    light_switch: shared sync object (LightSwitch)\n
    room: Semaphore initialized to value 1\n
    turnstile: Semaphore initialized to value 1

    Return value
    ------------
    None

    :param light_switch: shared sync object (LightSwitch)
    :param room: Semaphore initialized to value 1
    :param turnstile: Semaphore initialized to value 1
    """
    while True:
        turnstile.wait()
        turnstile.signal()
        light_switch.lock(room)
        sleep(randint(1, 10)/10)
        print("Reader is reading")
        light_switch.unlock(room)


def writer(room, turnstile):
    """
    Function representing writer writing to some shared document

    Parameters
    ----------
    room: Semaphore initialized to value 1\n
    turnstile: Semaphore initialized to value 1

    Return value
    ------------
    None

    :param room: Semaphore initialized to value 1
    :param turnstile: Semaphore initialized to value 1
    """
    while True:
        turnstile.wait()
        room.wait()
        sleep(randint(1, 10)/100)
        print("Writer is writing")
        room.signal()
        turnstile.signal()


def main():
    """
    Main function used for execution of code.

    :return: None
    """
    turnstile = Semaphore(1)
    room = Semaphore(1)
    switch = LightSwitch()
    r = [Thread(reader, switch, room, turnstile) for _ in range(10)]
    w = Thread(writer, room, turnstile)

    [t.join() for t in r]
    w.join()


if __name__ == "__main__":
    main()
