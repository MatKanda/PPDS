

def cat(f, next_fnc):
    next(next_fnc)
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(str, next_fnc):
    next(next_fnc)
    try:
        while True:
            line = yield
            next_fnc.send(line.count(str))
    except GeneratorExit:
        next_fnc.close()


def wc(str):
    cnt = 0
    try:
        while True:
            cnt += yield
    except GeneratorExit:
        print(cnt)


def dispatch(greps):
    """
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
