import asyncio
import sys

from aiohttp.client import ClientSession

from bot_telegram.utils.telegram_api import post_data


async def run(url: str):
    with ClientSession() as client:
        await post_data({
            'method': 'setWebhook',
            'url': url,
        }, client)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run(sys.argv[1]))