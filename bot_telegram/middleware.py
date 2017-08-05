from aiohttp import web
from mogiminsk.utils import Session

import logging
logger = logging.getLogger(__name__)


async def error_handler_middleware(app, handler):
    async def inner_handler(request):
        try:
            return await handler(request)
        except:
            logger.exception('Unexpected exception is muted.')
            return web.Response()

    return inner_handler


async def session_initializer_middleware(app, handler):
    async def inner_handler(request):
        request['db'] = Session()
        try:
            response = await handler(request)
        except Exception as e:
            logger.warning('Got unexpected exception session wil be rolled back.')
            request['db'].rollback()
            raise e

        request['db'].commit()
        request['db'].close()
        return response

    return inner_handler
