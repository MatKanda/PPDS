from fei.ppds import Thread, Semaphore, Mutex, print, Event


class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self. n:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()


def barrier_example(barrier, thread_id):
    print(f"thread {thread_id} before barrier")
    barrier.wait()
    print(f"thread {thread_id} after barrier")


def execute_code():
    THREADS = 15
    barrier = SimpleBarrier(THREADS)
    threads = [Thread(barrier_example, barrier, i) for i in range(THREADS)]
    [t.join() for t in threads]


for j in range(20):
    execute_code()
    print("---------------------------------")
