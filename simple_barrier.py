from fei.ppds import Thread, Semaphore, Mutex, print, Event


class SimpleBarrier:
    """
    SimpleBarrier class shared between threads.

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
        Create attributes for SimpleBarrier class.

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
        Wait method of SimpleBarrier class used to count threads and increment/decrement counter
        in purpose to release waiting threads.

        Return value
        ------------
        None
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self. n:
            self.counter = 0
            self.event.set()
        self.mutex.unlock()
        self.event.wait()


def barrier_example(barrier, thread_id):
    """
    Function simulating some program code to test barrier solution.

    Parameters
    ----------
    barrier -> class of SimpleBarrier object\n
    thread_id -> id of the thread currently using this function

    Return value
    ------------
    None

    :param barrier: class of SimpleBarrier object
    :param thread_id: id of the thread currently using this function
    """
    print(f"thread {thread_id} before barrier")
    barrier.wait()
    print(f"thread {thread_id} after barrier")


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
    barrier = SimpleBarrier(THREADS)
    threads = [Thread(barrier_example, barrier, i) for i in range(THREADS)]
    [t.join() for t in threads]


for j in range(20):
    execute_code()
    print("---------------------------------")
