"""
Roller coaster

This is the file representing multiple trains giving a ride to
multiple passengers. There can be only 1 train at the loading dock
and 1 train at the unloading dock at the same time. Passengers are
boarding and unboarding the trains.

It requires "fei.ppds", "time", "random" and "Barrier" imports.
"""

from fei.ppds import Semaphore, print, Thread
from Barrier import Barrier
from time import sleep
from random import randint


def board(passenger_name):
    """
    Function simulating boarding of passenger to the train.

    Parameters
    ----------
    passenger_name: name of boarding passenger

    Return value
    ------------
    None

    :param passenger_name: name of boarding passenger
    """
    print(f"Passenger {passenger_name} is boarding...")
    sleep(randint(1, 2))


def unboard(passenger_name):
    """
    Function simulating unboarding of passenger to the train.

    Parameters
    ----------
    passenger_name: name of unboarding passenger

    Return value
    ------------
    None

    :param passenger_name: name of unboarding passenger
    """
    print(f"Passenger {passenger_name} is unboarding...")
    sleep(randint(1, 2))


def load(train_id):
    """
    Function simulating loading the tran with passengers

    Parameters
    ----------
    train_id: name of the loaded train

    Return value
    ------------
    None

    :param train_id: name of the loaded train
    """
    print(f"Train {train_id} is loading passengers...")
    sleep(randint(1, 2))


def unload(train_id):
    """
    Function simulating unloading the tran with passengers

    Parameters
    ----------
    train_id: name of the unloaded train

    Return value
    ------------
    None

    :param train_id: name of the unloaded train
    """
    print(f"Train {train_id} is unloading passengers...")
    sleep(randint(1, 2))


def run(train_id):
    """
    Function simulating the tran giving a ride.

    Parameters
    ----------
    train_id: name of the train

    Return value
    ------------
    None

    :param train_id: name of the train
    """
    print(f"Train {train_id} is on its way...")
    sleep(3)


def next_id(id, number_of_trains):
    """
    Function used to compute next train id to load/unload.

    Parameters
    ----------
    id: id of the train
    number_of_trains: total number of trains

    Return value
    ------------
    None

    :param id: id of the train
    :param number_of_trains: total number of trains
    """
    return (id + 1) % number_of_trains


def train(board_q, boarded, unboard_q, unboarded, loading_area, unloading_area, train_id, passengers, trains):
    """
    Function simulating all activities done by train e.g. un/loading the passengers.

    Parameters
    ----------
    :param board_q: Board queue, Semaphore object
    :param boarded: Semaphore object used to wait for all passengers to board in
    :param unboard_q: Unboard queue, Semaphore object
    :param unboarded: Semaphore object used to wait for all passengers to unboard out
    :param loading_area: Array of Semaphores, decides which train can start loading
    :param unloading_area: Array of Semaphores, decides which train can start unloading
    :param train_id: Name of the train
    :param passengers: Total number of passenger
    :param trains: Total number of trains
    """
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
    """
    Function simulating boarding and unboarding the passenger on the train.

    Parameters
    ----------
    :param board_q: Board queue, Semaphore object
    :param boarded: Semaphore object used as an argument into the "board_b" barrier
    :param unboard_q: Unboard queue, Semaphore object
    :param unboarded: Semaphore object used to wait for all passengers to unboard out
    :param board_b: Barrier object used to wait for all passengers to board in, last one calls signal
    :param unboard_b: Barrier object used to wait for all passengers to unboard out, last one calls signal
    :param unboarded: Semaphore object used as an argument into the "unboard_b" barrier
    :param passenger_name: Name of current passenger
    """
    while True:
        board_q.wait()
        board(passenger_name)
        board_b.wait(boarded)

        unboard_q.wait()
        unboard(passenger_name)
        unboard_b.wait(unboarded)


def init():
    """
    Initialization of above functions.
    """
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
