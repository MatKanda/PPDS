"""

Authour: Matúš Kanda
License: MIT
"""
from time import sleep


def sending(data, s, w):
    next(s)
    next(w)
    for d in data:
        print("Sending data...")
        s.send(d)
    print("No more data.")
    print("\nExiting sending process...")
    s.close()
    w.close()


def receiving(w):
    try:
        while True:
            print("Waiting for data...")
            word = yield
            print(f"\tSent word was {word}.")
            w.send(word)
    except GeneratorExit:
        print("Exiting receiving process...")


def working():
    try:
        while True:
            print("Trying to work...")
            word = yield
            print(f"\tThe computer is working with {word}.")
    except GeneratorExit:
        print("Exiting working process...")


def scheduler(data):
    while True:
        w = working()
        s = receiving(w)
        f = sending(data, s, w)


if __name__ == "__main__":
    data = ["CPU", "GPU", "Network", "Keyboard", "Mouse"]
    scheduler(data)
