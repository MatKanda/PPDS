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


def load(train_id):
    print(f"Train {train_id} is loading passengers...")
    sleep(randint(1, 2))


def unload(train_id):
    print(f"Train {train_id} is unloading passengers...")
    sleep(randint(1, 2))


def run(train_id):
    print(f"Train {train_id} is on its way...")
    sleep(3)


def next_id(id, number_of_trains):
    return (id + 1) % number_of_trains


def train(board_q, boarded, unboard_q, unboarded, loading_area, unloading_area, train_id, passengers, trains):
    while True:
        loading_area[train_id].wait()
        load(train_id)
        board_q.signal(passengers)
        boarded.wait()
        loading_area[next_id(train_id, trains)].signal()
        run(train_id)
        unloading_area[train_id].wait()
        unload(train_id)
        unboard_q.signal(passengers)
        unboarded.wait()
        unloading_area[next_id(train_id, trains)].signal()


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
    c = 10
    # number of trains
    t = 3

    loading_area = [Semaphore(0) for i in range(t)]
    unloading_area = [Semaphore(0) for i in range(t)]
    loading_area[0].signal()
    unloading_area[0].signal()

    board_queue = Semaphore(0)
    board_barrier = Barrier(c)
    boarded = Semaphore(0)
    unboard_queue = Semaphore(0)
    unboard_barrier = Barrier(c)
    unboarded = Semaphore(0)

    passengers = [Thread(passenger, board_queue, board_barrier, boarded, unboard_queue, unboard_barrier, unboarded, i+1)
                  for i in range(c)]

    trains = [Thread(train, board_queue, boarded, unboard_queue, unboarded, loading_area, unloading_area, i, c, t)
              for i in range(t)]

    [t.join() for t in passengers + trains]


if __name__ == "__main__":
    init()
