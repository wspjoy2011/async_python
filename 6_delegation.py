class CustomException(Exception):
    pass


def coroutine(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


@coroutine
def sub_gen():
    while True:
        try:
            message = yield
        except StopIteration:
            print('Exception in sub_gen()', message)
        else:
            print('.....................', message)


@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except StopIteration as e:
    #         g.throw(e)
    yield from g


sg = sub_gen()
g = delegator(sg)

next(g)
g.send('Hello')
g.throw(StopIteration)
g.send('Finish')

