"""
Smokers

This is the file representing smokers waiting for
the resources needed to make and then to smoke cigarettes.
There are resource suppliers -> agents and pushers, who pass
the resources on the "table" from where the smokers can take it.

It requires "fei.ppds", "time" and "random" imports.
"""
from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, print


class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatch = Semaphore(0)

        self.mutex = Mutex()
        self.isTobacco = 0
        self.isMatch = 0
        self.isPaper = 0

        self.agentSem = Semaphore(1)


def make_cigarette(name):
    """
    Function to simulate making a cigarette.

    Parameters
    ----------
    name: name of the smoker

    Return value
    ------------
    None

    :param name: name of the smoker
    """
    print(f"smoker '{name}' makes cigarette")
    sleep(randint(0, 10) / 100)


def smoke(name):
    """
    Function to simulate smoking a cigarette.

    Parameters
    ----------
    name: name of the smoker

    Return value
    ------------
    None

    :param name: name of the smoker
    """
    print(f"smoker '{name}' smokes")
    sleep(randint(0, 10) / 100)


def smoker_match(shared):
    """
    Function to simulate smokers waiting for resources, make the cigarette
    and smoke it.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        shared.agentSem.signal()
        smoke("match")


def smoker_tobacco(shared):
    """
    Function to simulate smokers waiting for resources, make the cigarette
    and smoke it.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        shared.agentSem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    """
    Function to simulate smokers waiting for resources, make the cigarette
    and smoke it.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        shared.agentSem.signal()
        smoke("paper")


def agent_1(shared):
    """
    Function to simulate an agent providing the resources for pushers.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: tobacco, paper --> smoker 'match'")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    """
    Function to simulate an agent providing the resources for pushers.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: paper, match --> smoker 'tobacco'")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    """
    Function to simulate an agent providing the resources for pushers.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: tobacco, match --> smoker 'paper'")
        shared.tobacco.signal()
        shared.match.signal()


def pusher_match(shared):
    """
    Function where pusher is handling provided resources and either
    giving them to the smokers or putting it on the table.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        shared.match.wait()

        shared.mutex.lock()
        # randomize the priority when there are many resources
        if shared.isTobacco and shared.isPaper:
            tmp = randint(0, 1)
            if tmp == 0:
                shared.isTobacco -= 1
                shared.pusherPaper.signal()
            else:
                shared.isPaper -= 1
                shared.pusherTobacco.signal()
        else:
            if shared.isTobacco:
                shared.isTobacco -= 1
                shared.pusherPaper.signal()
            elif shared.isPaper:
                shared.isPaper -= 1
                shared.pusherTobacco.signal()
            else:
                shared.isMatch += 1
        shared.mutex.unlock()


def pusher_paper(shared):
    """
    Function where pusher is handling provided resources and either
    giving them to the smokers or putting it on the table.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        shared.paper.wait()

        shared.mutex.lock()
        # randomize the priority when there are many resources
        if shared.isTobacco and shared.isMatch:
            tmp = randint(0, 1)
            if tmp == 0:
                shared.isTobacco -= 1
                shared.pusherMatch.signal()
            else:
                shared.isMatch -= 1
                shared.pusherTobacco.signal()
        else:
            if shared.isTobacco:
                shared.isTobacco -= 1
                shared.pusherMatch.signal()
            elif shared.isMatch:
                shared.isMatch -= 1
                shared.pusherTobacco.signal()
            else:
                shared.isPaper += 1
        shared.mutex.unlock()


def pusher_tobacco(shared):
    """
    Function where pusher is handling provided resources and either
    giving them to the smokers or putting it on the table.

    Parameters
    ----------
    shared: shared sync Object "Shared"

    Return value
    ------------
    None

    :param shared: shared sync Object "Shared"
    """
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
        # randomize the priority when there are many resources
        if shared.isPaper and shared.isMatch:
            tmp = randint(0, 1)
            if tmp == 0:
                shared.isPaper -= 1
                shared.pusherMatch.signal()
            else:
                shared.isMatch -= 1
                shared.pusherPaper.signal()
        else:
            if shared.isPaper:
                shared.isPaper -= 1
                shared.pusherMatch.signal()
            elif shared.isMatch:
                shared.isMatch -= 1
                shared.pusherPaper.signal()
            else:
                shared.isTobacco += 1
        shared.mutex.unlock()


def run():
    shared = Shared()
    smokers = []
    pushers = []
    agents = []

    smokers.append(Thread(smoker_paper, shared))
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))

    pushers.append(Thread(pusher_paper, shared))
    pushers.append(Thread(pusher_match, shared))
    pushers.append(Thread(pusher_tobacco, shared))

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in smokers+pushers+agents:
        t.join()


if __name__ == "__main__":
    run()
