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


def philosopher_left(forks, p_id):
    sleep(randint(50, 100) / 1000)

    while True:
        think(p_id)
        get_forks_left(forks, p_id)
        eat(p_id)
        put_forks_left(forks, p_id)


def philosopher_right(forks, p_id):
    sleep(randint(50, 100) / 1000)

    while True:
        think(p_id)
        get_forks_right(forks, p_id)
        eat(p_id)
        put_forks_right(forks, p_id)


def think(p_id):
    print(f"{p_id} is thinking")
    sleep(randint(30, 40) / 1000)


def eat(p_id):
    print(f"{p_id} is eating")
    sleep(randint(30, 40) / 1000)


def get_forks_right(forks, p_id):
    print(f"{p_id} is trying to get forks")
    forks[p_id].wait()
    forks[(p_id+1) % PHILOSOPHERS].wait()
    print(f"{p_id} has taken the forks")


def put_forks_right(forks, p_id):
    forks[p_id].signal()
    forks[(p_id+1) % PHILOSOPHERS].signal()
    print(f"{p_id} has put the forks")


def get_forks_left(forks, p_id):
    print(f"{p_id} is trying to get forks")
    forks[(p_id+1) % PHILOSOPHERS].wait()
    forks[p_id].wait()
    print(f"{p_id} has taken the forks")


def put_forks_left(forks, p_id):
    forks[(p_id+1) % PHILOSOPHERS].signal()
    forks[p_id].signal()
    print(f"{p_id} has put the forks")


def main():
    forks = [Semaphore(1) for _ in range(PHILOSOPHERS)]

    phils_l = [Thread(philosopher_left, forks, p_id) for p_id in range(2)]
    phils_r = [Thread(philosopher_right, forks, p_id) for p_id in range(3)]

    for p in phils_l + phils_r:
        p.join()


if __name__ == "__main__":
    main()
