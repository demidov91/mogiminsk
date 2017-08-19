from mogiminsk.utils import Session, set_db


import logging
logger = logging.getLogger(__name__)


async def middleware(app, handler):
    async def inner_handler(request):
        request['db'] = Session()
        set_db(request['db'])
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
