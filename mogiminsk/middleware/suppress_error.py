from aiohttp import web

import logging
logger = logging.getLogger(__name__)


async def middleware(app, handler):
    async def inner_handler(request):
        try:
            return await handler(request)
        except:
            logger.exception('Unexpected exception is muted.')
            return web.Response()

    return inner_handler