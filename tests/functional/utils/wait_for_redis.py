import asyncio
import os

from aioredis import Redis
from backoff import backoff


@backoff()
async def main():
    redis = Redis(host=os.environ.get('REDIS_HOST'))

    while True:
        if await redis.ping():
            break


if __name__ == '__main__':
    asyncio.run(main())
