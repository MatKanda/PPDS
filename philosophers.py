"""
Philosophers

This is the file simulating philosophers sitting around the round table
and trying to eat at the same time. They need 2 forks for successful eating
but there is limited number of forks. Some philosophers need to wait for others
to put down the forks, so they can start eating.

This file requires "fei.ppds", "time" and "random" imports.
"""
from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


PHILOSOPHERS = 5


def create_philosophers(forks):
    """
    Function that creates philosophers based on the generated random number. It runs the threads as well to execute
    functions defined down below.

    Parameters
    ----------
    forks: List of Semaphores initialized to 1 representing forks

    Return value
    ------------
    None

    :param forks: List of Semaphores initialized to 1 representing forks
    """

    # random number of left-handed philosophers, at least 1, max all-1
    left_handed = randint(1, PHILOSOPHERS-1)

    phils_l = [Thread(philosopher, forks, p_id, "left") for p_id in range(0, left_handed)]
    phils_r = [Thread(philosopher, forks, p_id, "right") for p_id in range(left_handed, PHILOSOPHERS)]

    for p in phils_l + phils_r:
        p.join()


def philosopher(forks, p_id, hand):
    """
    Function representing philosopher who thinks, takes the forks, eats and then put the forks back.

    Parameters
    ----------
    forks: List of Semaphores initialized to 1 representing forks
    p_id: id of current philosopher
    hand: determines whether the philosopher is left or right-handed

    Return value
    ------------
    None

    :param forks: List of Semaphores initialized to 1 representing forks
    :param p_id: id of current philosopher
    :param hand: determines whether the philosopher is left or right-handed
    """
    sleep(randint(50, 100) / 1000)

    while True:
        think(p_id)
        get_forks(forks, p_id, hand)
        eat(p_id)
        put_forks(forks, p_id, hand)


def think(p_id):
    """
    Function simulating thinking philosopher.

    Parameters
    ----------
    p_id: id of current philosopher

    Return value
    ------------
    None

    :param p_id: id of current philosopher
    """
    print(f"{p_id} is thinking")
    sleep(randint(30, 40) / 1000)


def eat(p_id):
    """
    Function simulating eating philosopher.

    Parameters
    ----------
    p_id: id of current philosopher

    Return value
    ------------
    None

    :param p_id: id of current philosopher
    """
    print(f"{p_id} is eating")
    sleep(randint(30, 40) / 1000)


def get_forks(forks, p_id, hand):
    """
    Function simulating getting forks from the table.

    Parameters
    ----------
    forks: List of Semaphores initialized to 1 representing forks
    p_id: id of current philosopher
    hand: determines whether the philosopher is left or right-handed

    Return value
    ------------
    None

    :param forks: List of Semaphores initialized to 1 representing forks
    :param p_id: id of current philosopher
    :param hand: determines whether the philosopher is left or right-handed
    """
    print(f"{p_id} is trying to get forks")
    if hand == "right":
        forks[p_id].wait()
        forks[(p_id+1) % PHILOSOPHERS].wait()
    else:
        forks[(p_id + 1) % PHILOSOPHERS].wait()
        forks[p_id].wait()
    print(f"{p_id} has taken the forks")


def put_forks(forks, p_id, hand):
    """
    Function simulating putting forks back on the table.

    Parameters
    ----------
    forks: List of Semaphores initialized to 1 representing forks
    p_id: id of current philosopher
    hand: determines whether the philosopher is left or right-handed

    Return value
    ------------
    None

    :param forks: List of Semaphores initialized to 1 representing forks
    :param p_id: id of current philosopher
    :param hand: determines whether the philosopher is left or right-handed
    """
    if hand == "right":
        forks[p_id].signal()
        forks[(p_id + 1) % PHILOSOPHERS].signal()
    else:
        forks[(p_id+1) % PHILOSOPHERS].signal()
        forks[p_id].signal()
    print(f"{p_id} has put the forks")


def main():
    """
    Main function where the other functions are called.
    """
    forks = [Semaphore(1) for _ in range(PHILOSOPHERS)]

    create_philosophers(forks)


if __name__ == "__main__":
    main()
