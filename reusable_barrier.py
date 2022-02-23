from fei.ppds import Thread, Mutex, Event
from fei.ppds import print


class Barrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()

    def clear(self):
        self.event.clear()


def rendezvous(thread_name):
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)


def barrier_example(barrier1, barrier2, thread_name):
    while True:
        barrier1.clear()
        rendezvous(thread_name)
        barrier1.wait()
        barrier2.clear()
        ko(thread_name)
        barrier2.wait()


def execute_code():
    THREADS = 15
    threads = list()
    barrier1 = Barrier(THREADS)
    barrier2 = Barrier(THREADS)
    for i in range(THREADS):
        t = Thread(barrier_example, barrier1, barrier2, 'Thread %d' % i)
        threads.append(t)

    for t in threads:
        t.join()


for j in range(20):
    execute_code()
    print("---------------------------------")
