import asyncio
import sys

from aiohttp.client import ClientSession

from bot_viber import defines
from bot_viber.utils.viber_api import ViberSender


async def run(url: str):
    async with ClientSession() as client:
        await ViberSender(client).post_data(ViberSender.SET_WEBHOOK, {
            'url': url,
            "event_types": [
                defines.EVENT_TYPE_FAILED,
                defines.EVENT_TYPE_SUBSCRIBED,
                defines.EVENT_TYPE_UNSUBSCRIBED,
                defines.EVENT_TYPE_CONVERSATION_STARTED,
            ]
        })


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run(sys.argv[1]))