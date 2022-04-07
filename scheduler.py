"""
Simple first try of couroutines implementation.

Authour: Matúš Kanda
License: MIT
"""


def sending(data, s, w):
    """
    Function used to send data to waiting couroutines.

    Parameters
    ----------
    data: array of words
    s: another couroutine
    w: another couroutine

    :param data: array of words
    :param s: another couroutine
    :param w: another couroutine
    """
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
    """
    Function used to receive data from oen couroutine
    and forward them to another couroutine.

    Parameters
    ----------
    w: another couroutine

    :param w: another couroutine

    """
    try:
        while True:
            print("Waiting for data...")
            word = yield
            print(f"\tSent word was {word}.")
            w.send(word)
    except GeneratorExit:
        print("Exiting receiving process...")


def working():
    """
    End function colleting the data and simulating some work with it.
    """
    try:
        while True:
            print("Trying to work...")
            word = yield
            print(f"\tThe computer is working with {word}.")
    except GeneratorExit:
        print("Exiting working process...")


def scheduler(data):
    """
    Scheduler used to schedule next process, in this case one by one in loop.

    Parameters
    ----------
    data: array of words

    :param data: array of words
    """
    while True:
        w = working()
        s = receiving(w)
        sending(data, s, w)


if __name__ == "__main__":
    data = ["CPU", "GPU", "Network", "Keyboard", "Mouse"]
    scheduler(data)
