from fei.ppds import Thread, Mutex, Event, Semaphore, RandomSemaphore
from fei.ppds import print
from random import randint
from time import sleep
import time


class Synchronization:
    """
    Synchronization class shared between threads.

    Attributes
    ----------
    n -> number of threads
    counter -> counter for number of threads that reached certain point of execution
    mutex -> lock used in 'wait' method
    synchronization_object -> Object used to sync, Semaphore or Event
    """
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
        """
        Method used to get current counter value.

        Return value
        ------------
        counter
        """
        return self.counter

    def increment_counter(self):
        """
        Method used to increment counter by 1

        Return value
        ------------
        None
        """
        self.counter += 1


def compute_fib(sync, i):
    """
    Function to compute Fibonacci consequence.

    Parameters
    ----------
    sync: Synchronization object\n
    i: Current thread accessing the function

    Return value
    ------------
    None

    :param sync: Synchronization object
    :param i: Current thread accessing the function
    """

    # exit if counter exceeded number of elements in sequence
    if sync.get_counter() >= THREADS:
        exit()
    sleep(randint(1, 10) / 10)

    # wait for all threads
    sync.wait(i)

    # compute if correct thread enters the function
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

# create Synchronization object
sync_obj = Synchronization(THREADS, sync_obj_semaphore)

threads = [Thread(compute_fib, sync_obj, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)

print("--- %s seconds ---" % (time.time() - start_time))
