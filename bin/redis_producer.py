import asyncio
from uuid import uuid4

import aioredis


async def main():
    pool = await aioredis.create_redis_pool(
        'redis://localhost', encoding='utf8', password='p4ssw0rd'
    )

    while True:
        print('.', end='')
        add_task = pool.xadd('message', {'access_id': str(uuid4())}, max_len=10)
        sleep_task = asyncio.sleep(5)

        await asyncio.gather(add_task, sleep_task)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
