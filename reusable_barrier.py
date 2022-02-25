from fei.ppds import Thread, Mutex, Event
from fei.ppds import print


class Barrier:
    """
    Barrier class shared between threads.

    Attributes
    ----------
    n -> number of threads
    counter -> counter for number of threads that reached certain point of execution
    mutex -> lock used in 'wait' method
    event -> event used to send signals for threads to wait/don't wait

    Return value
    ------------
    None
    """
    def __init__(self, n):
        """
       Create attributes for Barrier class.

       Parameters
       ----------
       n -> number of threads
       """
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
        Wait method of Barrier class used to count threads and increment/decrement counter
        in purpose to release waiting threads.

        Return value
        ------------
        None
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()

    def clear(self):
        """
        Clear method of Barrier class used to reset event settings.

        Return value
        ------------
        None
        """
        self.event.clear()


def rendezvous(thread_name):
    """
    Function used to simulate some program code before critical area for test purpose.

    Parameters
    ----------
    thread_name: Name of thread currently using this function

    Return value
    ------------
    None

    :param thread_name: Name of thread currently using this function
    """
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    """
    Function used to simulate some program code of critical area for test purpose.

    Parameters
    ----------
    thread_name: Name of thread currently using this function

    Return value
    ------------
    None

    :param thread_name: Name of thread currently using this function
    """
    print('ko: %s' % thread_name)


def barrier_example(barrier1, barrier2, thread_name):
    """
    Function simulating some program code to test barrier solution.

    Parameters
    ----------
    barrier1 -> class of SimpleBarrier object\n
    barrier2 -> id of the thread currently using this function\n
    thread_name -> Name of thread currently using this function

    Return value
    ------------
    None

    :param barrier1: class of SimpleBarrier object number 1
    :param barrier2: class of SimpleBarrier object number 2
    :param thread_name: Name of thread currently using this function
    """
    while True:
        barrier1.clear()
        rendezvous(thread_name)
        barrier1.wait()
        barrier2.clear()
        ko(thread_name)
        barrier2.wait()


def execute_code():
    """
    Function used to execute solution using functions and Classes

    Parameters
    ----------
    None

    Return value
    ------------
    None
    """
    THREADS = 15
    threads = list()
    barrier1 = Barrier(THREADS)
    barrier2 = Barrier(THREADS)
    for i in range(THREADS):
        t = Thread(barrier_example, barrier1, barrier2, 'Thread %d' % i)
        threads.append(t)

    for t in threads:
        t.join()


execute_code()
