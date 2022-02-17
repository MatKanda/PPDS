from collections import Counter
from fei.ppds import Thread
import threading


lock = threading.Lock()


class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


# incrementing every index of given array using locks because of multi threads
def do_count(shared):
    lock.acquire()
    while shared.counter != shared.end:
        # this if statement is used to ensure not to access array out of his range
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
    lock.release()


# joined block of code for easier function call from main class in another file
def execution_two():
    shared = Shared(1_000_000)
    t1 = Thread(do_count, shared)
    t2 = Thread(do_count, shared)
    t1.join()
    t2.join()

    counter = Counter(shared.elms)
    print(counter.most_common())
