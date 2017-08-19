from mogiminsk.utils import clear_local_data


import logging
logger = logging.getLogger(__name__)


async def middleware(app, handler):
    async def inner_handler(request):
        clear_local_data()
        response = await handler(request)
        clear_local_data()
        return response

    return inner_handler
