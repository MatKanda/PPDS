from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class LightSwitch(object):
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()
        self.room = Semaphore(1)

    def lock(self):
        self.mutex.lock()
        if not self.counter:
            self.room.wait()
        self.counter += 1
        self.mutex.unlock()

    def unlock(self):
        self.mutex.lock()
        self.counter -= 1
        if not self.counter:
            self.room.signal()
        self.mutex.unlock()


def reader(light_switch):
    while True:
        light_switch.lock()
        sleep(randint(1, 10)/10)
        print("Reader is reading")
        light_switch.unlock()


def writer(light_switch):
    while True:
        light_switch.room.wait()
        sleep(randint(1, 10)/100)
        print("Writer is writing")
        light_switch.room.signal()


def main():
    room = LightSwitch()
    w = [Thread(writer, room)]
    r = [Thread(reader, room) for _ in range(10)]

    [t.join() for t in w+r]


if __name__ == "__main__":
    main()
