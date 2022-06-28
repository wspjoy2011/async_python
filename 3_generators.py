from time import time, sleep


def gen1(s: str):
    for char in s:
        yield char


def gen2(n: int):
    for i in range(1, n+1):
        yield i


g1 = gen1('john')
g2 = gen2(10)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        tmp = next(task)
        print(tmp)
        tasks.append(task)
    except StopIteration:
        pass


def gen_filename():
    while True:
        pattern = "file-{}.jpeg"
        t = int(time() * 1000)
        yield pattern.format(t)

        pattern = pattern.split('.')[0].format(t)
        yield pattern


g = gen_filename()
