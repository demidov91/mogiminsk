import asyncio
import sys

from aiohttp.client import ClientSession

from bot_viber.utils.viber_api import ViberSender


async def run(url: str):
    with ClientSession() as client:
        await ViberSender(client).post_data(ViberSender.SET_WEBHOOK, {
            'url': url,
            "event_types": [
                "failed",
                "subscribed",
                "unsubscribed",
                "conversation_started"
            ]
        })


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run(sys.argv[1]))