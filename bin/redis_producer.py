import asyncio
from uuid import uuid4

import aioredis


async def main():
    pool = await aioredis.create_redis_pool(
        'redis://localhost', encoding='utf8', password='p4ssw0rd'
    )

    while True:
        print('.', end='')
        await pool.xadd('message', {'access_id': str(uuid4())}, max_len=10)
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
