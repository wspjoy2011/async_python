import asyncio
from time import time


async def print_nums():
    count = 0
    while True:
        print(count)
        count += 1
        await asyncio.sleep(0.5)


async def print_time():
    start = int(time())
    while True:
        now = int(time())
        if (now - start) % 3 == 0:
            print(f'{now - start} seconds have passed.')
        await asyncio.sleep(1)


async def main():
    task_nums = asyncio.create_task(print_nums())
    task_time = asyncio.create_task(print_time())

    await asyncio.gather(task_nums, task_time)


if __name__ == '__main__':
    asyncio.run(main())

