from fei.ppds import Semaphore, Mutex, print, Thread
from Barrier import Barrier
from time import sleep


class Molecule(object):
    def __init__(self):
        self.oxygen = 0
        self.hydrogen = 0
        self.mutex = Mutex()
        self.oxygen_queue = Semaphore(0)
        self.hydrogen_queue = Semaphore(0)
        self.barrier = Barrier(3)

    def inc_oxygen(self):
        self.oxygen += 1
        print(f"Inc oxygen, currently: {self.oxygen}")

    def inc_hydrogen(self):
        self.hydrogen += 1
        print(f"Inc hydrogen, currently: {self.hydrogen}")

    def dec_oxygen(self):
        self.oxygen -= 1

    def dec_hydrogen(self):
        self.hydrogen -= 2


def bond():
    print("H2O molecule created.\n")
    sleep(3)


def oxygen(molecule):
    while True:
        molecule.mutex.lock()
        molecule.inc_oxygen()

        if molecule.hydrogen < 2:
            molecule.mutex.unlock()
        else:
            molecule.dec_oxygen()
            molecule.dec_hydrogen()
            molecule.oxygen_queue.signal()
            molecule.hydrogen_queue.signal(2)

        molecule.oxygen_queue.wait()
        bond()

        molecule.barrier.wait_2_0()
        molecule.mutex.unlock()


def hydrogen(molecule):
    while True:
        molecule.mutex.lock()
        molecule.inc_hydrogen()
        if molecule.hydrogen < 2 or molecule.oxygen < 1:
            molecule.mutex.unlock()
        else:
            molecule.dec_hydrogen()
            molecule.dec_oxygen()
            molecule.oxygen_queue.signal()
            molecule.hydrogen_queue.signal(2)

        molecule.hydrogen_queue.wait()
        bond()

        molecule.barrier.wait_2_0()


def init():
    molecule = Molecule()

    ox = [Thread(oxygen, molecule) for i in range(1)]

    hydr = [Thread(hydrogen, molecule)for i in range(2)]

    [t.join() for t in ox + hydr]


if __name__ == "__main__":
    init()
