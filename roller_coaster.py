from fei.ppds import Semaphore, Mutex, print, Thread
from Barrier import Barrier
from time import sleep
from random import randint


def board(passenger_name):
    print(f"Passenger {passenger_name} is boarding...")
    sleep(randint(1, 2))


def unboard(passenger_name):
    print(f"Passenger {passenger_name} is unboarding...")
    sleep(randint(1, 2))


def load():
    print("Train is loading passengers...")
    sleep(randint(1, 2))


def unload():
    print("Train is unloading passengers...")
    sleep(randint(1, 2))


def run():
    print("Train is on its way...")
    sleep(3)


def train(board_q, boarded, unboard_q, unboarded, c):
    while True:
        load()
        board_q.signal(c)
        boarded.wait()

        run()

        unload()
        unboard_q.signal(c)
        unboarded.wait()


def passenger(board_q, board_b, boarded, unboard_q, unboard_b, unboarded, passenger_name):
    while True:
        board_q.wait()
        board(passenger_name)
        board_b.wait(boarded)

        unboard_q.wait()
        unboard(passenger_name)
        unboard_b.wait(unboarded)


def init():
    # number of passengers
    c = 5

    board_queue = Semaphore(0)
    board_barrier = Barrier(c)
    boarded = Semaphore(0)
    unboard_queue = Semaphore(0)
    unboard_barrier = Barrier(c)
    unboarded = Semaphore(0)

    passengers = [Thread(passenger, board_queue, board_barrier, boarded, unboard_queue, unboard_barrier, unboarded, i+1)
                  for i in range(c)]

    trains = [Thread(train, board_queue, boarded, unboard_queue, unboarded, c)]

    [t.join() for t in passengers + trains]


if __name__ == "__main__":
    init()
