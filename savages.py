"""
Savages

This is the file representing savages eating from the same pot.
If there is no food left, they need to call the cook to cook
full amount of food into the pot. Then they can eat again.

It requires "fei.ppds", "time" and "random" imports.
"""
from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

"""
M and N -> model parameters
M - number of food portions which fits into the pot
N - number of savages
C - number of cooks
"""
M = 2
N = 3
C = 3


class SimpleBarrier:
    """
    Mr. Jokay SimpleBarrier implementation for special prints
    in "wait()" method.
    Class used to wait for all threads and then to release them
    all at the same time.
    """

    def __init__(self, n):
        self.n = n
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self, print_str, savage_id, print_last_thread=False, print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.n:
            self.cnt = 0
            if print_last_thread:
                print(print_str % savage_id)
            self.sem.signal(self.n)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    """
    Object shared between Threads containing Mutex, counter and
    Semaphores and SimpleBarrier objects.
    """

    def __init__(self):
        self.mutex = Mutex()
        self.mutex_cooks = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.cook_barrier = SimpleBarrier(C)
        self.turnstile = Semaphore(1)
        self.to_cook = False
        self.counter = 0
        self.portions = 0

    def add_serving(self, cook_id):
        """
        Method used to increment number of servings. Last Thread which fills entire
        pot sends signal to the savages, so they can start eating.
        """
        self.mutex_cooks.lock()
        if self.servings < M and self.to_cook is True:
            # self.turnstile.signal()
            self.servings += 1
            print(f"kuchar {cook_id}: varim 1 porciu")
        else:
            self.to_cook = False
            print(f"kuchar {cook_id}: nevarim, je plny hrniec")
        if self.servings == M:
            self.full_pot.signal()
        self.mutex_cooks.unlock()


def get_serving_from_pot(savage_id, shared):
    """
    Function simulating getting a serving from shared pot.

    Parameters
    ----------
    savage_id: id of savage currently taking a serving
    shared: shared sync object used to access common data

    Return value
    ------------
    None

    :param savage_id: id of savage currently taking a serving
    :param shared: shared sync object used to access common data
    """

    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    """
    Function simulating eating.

    Parameters
    ----------
    savage_id: id of savage currently taking a serving

    Return value
    ------------
    None

    :param savage_id: id of savage currently taking a serving
    """
    print("divoch %2d: hodujem" % savage_id)
    # process of eating
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    """
    Function simulating savages eating from the pot.
    The "if" part is checking whether the pot is empty or not
    and call the cook to cook another full pot if needed.

    Parameters
    ----------
    savage_id: id of savage currently taking a serving
    shared: shared sync object used to access common data

    Return value
    ------------
    None

    :param savage_id: id of savage currently taking a serving
    :param shared: shared sync object used to access common data
    """
    while True:
        # Before every start of dinner, they have to wait for all
        # savages to come. That's why we use barrier here.
        shared.barrier1.wait(
            "divoch %2d: prisiel som na veceru, uz nas je %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                             savage_id,
                             print_last_thread=True)
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        shared.to_cook = False
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.to_cook = True
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
            shared.to_cook = False
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def put_servings_in_pot(m, cook_id, shared):
    """
    Function simulating putting servings into to pot.

    Parameters
    ----------
    m: number of portions to cook
    cook_id: id of current cook
    shared: shared sync object used to access common data

    Return value
    ------------
    None

    :param m: number of portions to cook
    :param cook_id: id of current cook
    :param shared: shared sync object used to access common data
    """
    for i in range(0, m):
        # shared.turnstile.wait()
        shared.add_serving(cook_id)
        # cooking the meal
        sleep(0.4 + randint(0, 2) / 10)


def cook(m, cook_id, shared):
    """
    Function simulating cooking another pot of meal.

    Parameters
    ----------
    m: number of portions to cook
    cook_id: id of current cook
    shared: shared sync object used to access common data

    Return value
    ------------
    None

    :param m: number of portions to cook
    :param cook_id: id of current cook
    :param shared: shared sync object used to access common data
    """

    shared.cook_barrier.wait("kuchar %2d: caka na ostatnych kucharov,"
                             " je nas %2d", cook_id, print_each_thread=True)
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(m, cook_id, shared)
        shared.full_pot.signal()


def init_and_run(n, m, c):
    """
    Function to run a code which is being called from main.

    Parameters
    ----------
    n: number of savages
    m: number of food servings
    c: number of cooks

    Return value
    ------------
    None

    :param n: number of savages
    :param m: number of food servings
    :param c: number of cooks
    """
    threads = list()
    shared = Shared()
    room = Semaphore(1)
    for savage_id in range(0, n):
        threads.append(Thread(savage, savage_id, shared))
    for cook_id in range(0, c):
        threads.append(Thread(cook, m, cook_id, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M, C)
