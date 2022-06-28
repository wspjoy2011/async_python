from inspect import getgeneratorstate


def sub_gen():
    hello = 'Ready to accept message'
    message = yield hello
    print(f'Subgen received: {message}')


# gen = sub_gen()

# print(getgeneratorstate(gen))
# print(gen.send(None))
# print(getgeneratorstate(gen))
# print(gen.send('Hello, world!'))

def coroutine(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


@coroutine
def calc_average():
    count = 0
    sum = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration as e:
            print(f'Average: {e.value}')
            print('Done')
            break
        else:
            count += 1
            sum += x
            average = round(sum / count, 2)
    return average


gen = calc_average()
print(gen.send(10))
print(gen.send(5))
print(gen.send(7))

print(gen.throw(StopIteration))

