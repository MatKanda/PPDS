"""
Water molecule

This is the file where multiple threads are creating H2O molecule
by incrementing oxygen and hydrogen elements one by one.

It requires "fei.ppds", "time" and "Barrier" imports.
"""

from fei.ppds import Semaphore, Mutex, print, Thread
from Barrier import Barrier
from time import sleep


class Molecule(object):
    """
    Shared Molecule class.

    Attributes
    ----------
    oxygen -> number of oxygens
    hydrogen -> number of hydrogens
    mutex -> Mutex object
    oxygen_queue -> Semaphore object for oxygens
    hydrogen_queue -> Semaphore object for hydrogens
    barrier -> Barrier object
    """
    def __init__(self):
        self.oxygen = 0
        self.hydrogen = 0
        self.mutex = Mutex()
        self.oxygen_queue = Semaphore(0)
        self.hydrogen_queue = Semaphore(0)
        self.barrier = Barrier(3)

    def inc_oxygen(self):
        """
        Incrementation of oxygen parameter.
        """
        self.oxygen += 1
        print(f"Inc oxygen, currently: {self.oxygen}")

    def inc_hydrogen(self):
        """
        Incrementation of hydrogen parameter.
        """
        self.hydrogen += 1
        print(f"Inc hydrogen, currently: {self.hydrogen}")

    def dec_oxygen(self):
        """
        Decrementation of oxygen parameter
        """
        self.oxygen -= 1

    def dec_hydrogen(self):
        """
        Decrementation of hydrogen parameter
        """
        self.hydrogen -= 2


def bond():
    """
    Connect H and O into the H2O molecule.
    """
    print("H2O molecule created.\n")
    sleep(3)


def oxygen(molecule):
    """
    Function generating oxygens and waiting for hydrogens to be able to create H2O molecule:

    Parameters
    ----------
    molecule: Shared Molecule object

    :param molecule:
    """
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
    """
    Function generating hydrogens and waiting for oxygens to be able to create H2O molecule:

    Parameters
    ----------
    molecule: Shared Molecule object

    :param molecule:
    """
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
    """
    Initialization of above functions.
    """
    molecule = Molecule()

    ox = [Thread(oxygen, molecule) for i in range(1)]

    hydr = [Thread(hydrogen, molecule)for i in range(2)]

    [t.join() for t in ox + hydr]


if __name__ == "__main__":
    init()
