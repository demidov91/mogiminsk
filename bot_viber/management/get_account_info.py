import asyncio

from aiohttp.client import ClientSession

from bot_viber.utils.viber_api import ViberSender


async def run():
    async with ClientSession() as client:
        await ViberSender(client).post_data(ViberSender.GET_ACCOUNT_INFO, {})


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())