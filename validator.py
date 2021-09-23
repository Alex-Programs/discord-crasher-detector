import subprocess
from threading import *
import aiohttp
import aiofiles
import concurrent.futures
import asyncio
import os
from random import *

executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=32,
)

def video_is_corrupt(path):
    stdout = subprocess.run(["ffmpeg.exe", "-i", path, "-f", "null", "-"], capture_output=True)
    if "null @" in str(stdout.stderr):
        print("Corrupt due to null @ in stderr")
        return True

    elif "null @" in str(stdout.stdout):
        print("Corrupt due to null @ in stdout")
        return True

    elif stdout.returncode != 0:
        print("Corrupt due to nonzero return code")
        return True
    else:
        return False

async def get_and_check(path):
    session = aiohttp.ClientSession()

    name = str(choice(range(1, 100000))) + str(choice(range(1, 100000))) + str(choice(range(1, 100000))) + str(choice(range(1, 100000)))
    async with session.get(path) as resp:
        f = await aiofiles.open(name, mode='wb')
        await f.write(await resp.read())
        await f.close()
    
    result = parse_asyncio(str(await asyncio.wait([asyncio.get_event_loop().run_in_executor(executor, video_is_corrupt, name)])))
    await session.close()

    os.remove(name)

    return result

def parse_asyncio(i):
    if "True" in i:
        return True
    else:
        return False

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(get_and_check("https://thumbs.gfycat.com/TartAdolescentBird-mobile.mp4"))
    asyncio.get_event_loop().run_forever()
