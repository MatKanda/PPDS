from fei.ppds import Thread, Mutex, Semaphore, print


class LightSwitch(object):
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        if not self.counter:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if not self.counter:
            semaphore.signal()
        self.mutex.unlock()


def main():
    print("main")


if __name__ == "__main__":
    main()

