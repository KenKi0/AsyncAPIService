import asyncio
import time

from aioredis import Redis


async def main():
    redis = Redis(host='redis')

    while True:
        if await redis.ping():
            break
        time.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
