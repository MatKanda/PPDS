from fei.ppds import Thread, Mutex, Event
from fei.ppds import print
from random import randint
from time import sleep


def compute_fib(i):
    sleep(randint(1, 10)/10)
    # wait
    fib_seq[i+2] = fib_seq[i] + fib_seq[i+1]


THREADS = 10
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

threads = [Thread(compute_fib, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)
