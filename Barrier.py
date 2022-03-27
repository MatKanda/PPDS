from fei.ppds import Mutex, Event


class Barrier:
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

    def wait(self, sem):
        """
        Wait method of Barrier class used to count threads and increment/decrement counter
        in purpose to release waiting threads.

        Parameters
        ----------
        sem: Semaphore Object, last thread calls signal on it

        :param sem: Semaphore Object, last thread calls signal on it
        Return value
        ------------
        None
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self. n:
            self.counter = 0
            sem.signal()
            self.event.set()
        self.mutex.unlock()
        self.event.wait()

    def wait_2_0(self):
        """
        Wait method of Barrier class used to count threads and increment/decrement counter
        in purpose to release waiting threads. Same as above just without Semaphore Object.

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
