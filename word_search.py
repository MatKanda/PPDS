"""
Example usage of Couroutines used to read and count number of substrings in given file.

Authour: Matúš Jókay
License: MIT
"""


def cat(f, next_fnc):
    """
    Function to read file line by line.
    Every line is send to next_fnc()
    After the reading is done, sends GeneratorExit
    exception (.close()) to next_fnc()

    Parameters
    ----------
    f: file to read
    next_fnc: couroutine waiting for data

    :param f: file to read
    :param next_fnc: couroutine waiting for data
    """
    next(next_fnc)
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(str, next_fnc):
    """
    Couroutine waiting for line from the file, after getting the data
    sends substring occurrence (str input) to another couroutine.
    After receiving GeneratorExit exception it forwards it to
    next couroutine .

    Parameters
    ----------
    str: substring to search\n
    next_fnc: next couroutine waiting for data

    :param str: substring to search
    :param next_fnc: next couroutine waiting for data
    """
    next(next_fnc)
    try:
        while True:
            line = yield
            next_fnc.send(line.count(str))
    except GeneratorExit:
        next_fnc.close()


def wc(str):
    """
    Couroutine waiting for substring occurrence in line. Increments the number
    after receiving the data, exits the execution after receiving exception.

    Parameters
    ----------
    str: substring to search

    :param str: substring to search
    """
    cnt = 0
    try:
        while True:
            cnt += yield
    except GeneratorExit:
        print(f"{str}: {cnt}")


def dispatch(greps):
    """
    Koprogram, ktory caka na pocet vyskytov podretazca v riadku.

    Akonahle dostane pocet, pripocitava ho k celkovemu vysledku.
    Po obdrzani vynimky GeneratorExit cinnost koprogramu konci
    vypisom vysledku na obrazovku.
    """
    try:
        while True:
            line = (yield)
            for grep in greps:
                grep.send(line)
    except GeneratorExit:
        for grep in greps:
            grep.close()


if __name__ == "__main__":
    f = open("file.txt")
    substrings = ["a", "b", "y", "t"]
    greps = []
    for substring in substrings:
        w = wc(substring)
        g = grep(substring, w)
        greps.append(g)

    d = dispatch(greps)
    next(d)
    cat(f, d)
