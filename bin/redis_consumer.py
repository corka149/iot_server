import asyncio
import pprint

import aioredis

LAST_ID = '$'


async def main():
    redis = await aioredis.from_url(
        'redis://localhost', encoding='utf-8', password='p4ssw0rd', db=1, decode_responses=True
    )

    while True:
        streams_with_messages = await redis.xread(
            {'iot_messages': LAST_ID}, count=1, block=1
        )

        for stream, messages in streams_with_messages:
            for id_, m in messages:
                print(stream)
                pprint.pprint(m)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
