import asyncio
import sys

from aiohttp.client import ClientSession

from bot_telegram.utils.telegram_api import TgSender


async def run(url: str):
    async with ClientSession() as client:
        await TgSender(None, client, None).post_data({
            'method': 'setWebhook',
            'url': url,
        })


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run(sys.argv[1]))