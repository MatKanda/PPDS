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
    print(f"smoker '{name}' makes cigarette")
    sleep(randint(0, 10) / 100)


def smoke(name):
    print(f"smoker '{name}' smokes")
    sleep(randint(0, 10) / 100)


def smoker_match(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        shared.agentSem.signal()
        smoke("match")


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        shared.agentSem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        shared.agentSem.signal()
        smoke("paper")


def agent_1(shared):
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: tobacco, paper --> smoker 'match'")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: paper, match --> smoker 'tobacco'")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: tobacco, match --> smoker 'paper'")
        shared.tobacco.signal()
        shared.match.signal()


def pusher_match(shared):
    while True:
        shared.match.wait()

        shared.mutex.lock()
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
    while True:
        shared.paper.wait()

        shared.mutex.lock()
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
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
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
