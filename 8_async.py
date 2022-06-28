import requests
import os
import shutil
from time import time
import asyncio
import aiohttp


URL = 'https://loremflickr.com/320/240'
count = 1

# ########Sync##############


def clear_folder():
    folder = './img'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print(f"{filename} deleted.")
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_file(url):
    response = requests.get(url, allow_redirects=True)
    print(f'File downloaded')
    return response


def write_file(response):
    filename = response.url.split('/')[-1]
    with open(f'img/{filename}', 'wb') as f:
        f.write(response.content)
        print(f"{filename}_test.jpeg saved")


def main(qty=1):
    clear_folder()
    start = time()
    for _ in range(qty):
        file = get_file(URL)
        write_file(file)
    end = time()
    print(f"Time: {end - start}")


# ########Async##############


def write_content(data):
    filename = "file-{}.jpeg".format(int(time() * 1000))
    with open(f"img/{filename}", "wb") as f:
        f.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_content(data)


async def async_main(qty=1):
    tasks = []
    t0 = time()
    async with aiohttp.ClientSession() as session:
        for _ in range(qty):
            task = asyncio.create_task(fetch_content(URL, session))
            tasks.append(task)

        await asyncio.gather(*tasks)
    print(f"Time async: {time() - t0}")

if __name__ == "__main__":
    main(10)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(async_main(10))
