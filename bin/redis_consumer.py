import asyncio
import pprint

import aioredis

LAST_ID = '$'


async def main():
    pool = await aioredis.create_redis_pool(
        'redis://localhost', encoding='utf8', password='p4ssw0rd'
    )

    while True:
        messages = await pool.xread(
            ['message'], latest_ids=[LAST_ID], timeout=0, count=10
        )

        for m in messages:
            pprint.pprint(m)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
