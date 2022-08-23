import asyncio
import os
import time

from aioredis import Redis


async def main():
    redis = Redis(host=os.environ.get('ELASTIC_HOST'))

    while True:
        if await redis.ping():
            break
        time.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
