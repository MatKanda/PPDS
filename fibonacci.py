from fei.ppds import Thread, Mutex, Event, Semaphore, RandomSemaphore
from fei.ppds import print
from random import randint
from time import sleep
import time


class Synchronization:
    def __init__(self, n, synchronization_object):
        self.n = n
        self.synchronization_object = synchronization_object
        self.counter = 0
        self.mutex = Mutex()

    def wait(self, thread_index):
        """
        Wait method of Synchronization class used to stop and let go different threads

        Return value
        ------------
        None
        """
        self.mutex.lock()
        if thread_index == self.counter:
            if type(self.synchronization_object) is RandomSemaphore:
                self.synchronization_object.signal(self.n)
            if type(self.synchronization_object) is Event:
                self.synchronization_object.set()
        self.mutex.unlock()
        self.synchronization_object.wait()

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


# executable code
start_time = time.time()

THREADS = 15
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

# example usage with Event
sync_obj_event = Event()

# example usage with Semaphore
sync_obj_semaphore = Semaphore(0)

semaphore = Synchronization(THREADS, sync_obj_semaphore)
threads = [Thread(compute_fib, semaphore, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)

print("--- %s seconds ---" % (time.time() - start_time))
