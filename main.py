

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


def wc():
    cnt = 0
    try:
        while True:
            cnt += yield
    except GeneratorExit:
        print(cnt)


if __name__ == "__main__":
    f = open("file.txt")
    w = wc()
    g = grep("a", w)
    cat(f, g)
