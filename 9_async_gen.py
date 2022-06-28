import asyncio

# ####Async#####

# async def run_counter():
#     count = 0
#
#     while True:
#         print(count)
#         count += 1
#         await asyncio.sleep(1)
#
#
# async def say_hello():
#     count = 0
#
#     while True:
#         if count % 3 == 0:
#             print('Hello!')
#         count += 1
#         await asyncio.sleep(1)
#
#
# async def main():
#     task_count = asyncio.create_task(run_counter())
#     task_say_hello = asyncio.create_task(say_hello())
#
#     await asyncio.gather(task_count, task_say_hello)

# if __name__ == '__main__':
#     asyncio.run(main())


# ####Generators####

from time import sleep

queue = []


def run_counter():
    count = 0

    while True:
        print(count)
        count += 1
        yield


def say_hello():
    count = 0

    while True:
        if count % 3 == 0:
            print('Hello!')
        count += 1
        yield


def main_gen():
    while True:
        gen = queue.pop(0)
        next(gen)
        queue.append(gen)
        sleep(0.4)


if __name__ == "__main__":
    g_counter = run_counter()
    g_say_hello = say_hello()

    queue.extend([g_counter, g_say_hello])

    main_gen()
