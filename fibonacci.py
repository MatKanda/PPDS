from fei.ppds import Thread, Mutex, Event, Semaphore
from fei.ppds import print
from random import randint
from time import sleep


class Synchronization:
    def __init__(self, n):
        self.n = n
        self.semaphore = Semaphore(0)
        self.counter = 0
        self.mutex = Mutex()

    def wait(self, thread_index):
        """
        Wait method of Synchronization class used to count threads and increment/decrement counter
        in purpose to release waiting threads.

        Return value
        ------------
        None
        """
        self.mutex.lock()
        if thread_index == self.counter:
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()

    def get_counter(self):
        return self.counter

    def increment_counter(self):
        self.counter += 1


def compute_fib(sync, i):
    if sync.get_counter() >= THREADS:
        exit()
    sleep(randint(1, 10) / 10)
    sync.wait(i)
    if i == sync.get_counter():
        fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]
        sync.increment_counter()
        compute_fib(sync, i)
    else:
        compute_fib(sync, i)


THREADS = 10
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

# sync_obj = Synchronization(THREADS, Semaphore(0))
semaphore = Synchronization(THREADS)

threads = [Thread(compute_fib, semaphore, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)
