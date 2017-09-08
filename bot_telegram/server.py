import asyncio
import logging
import sys

from aiohttp import web

from bot_telegram.utils.states_helper import get_state, get_error_message
from bot_telegram.utils.telegram_helper import Update, get_or_create_user, TgSender
from mogiminsk.utils import init_client, destroy_client
from mogiminsk.middleware import (
    block_ip,
    initilize_session,
    suppress_error,
    clear_tasklocal,
)
from mogiminsk.settings import TELEGRAM_API_KEY

logger = logging.getLogger(__name__)


async def telegram_webhook(request):
    data = await request.json()
    update = Update.create(data)
    request['user'] = get_or_create_user(request['db'], update.get_user())
    if not (update.message or update.callback_query):
        raise ValueError('Got unexpected message type: {}'.format(update))

    state = get_state(request['user'])

    try:
        await state.consume(update.get_common_message())
        bot_messages = await state.produce()
    except Exception as e:
        logger.exception(e)
        bot_messages = get_error_message()
        request['user'].telegram_context = {'state': 'where'}

    connector = TgSender(update.get_chat().id, request.app['client'], request['user'])
    asyncio.ensure_future(
        connector.send_messages(bot_messages, update.get_message().id if update.callback_query else None)
    )

    if update.callback_query:
        return web.json_response({
            'method': 'answerCallbackQuery',
            'callback_query_id': update.callback_query.id,
        })

    return web.Response()


def init(argv):
    app = web.Application(middlewares=[
        suppress_error.middleware,
        clear_tasklocal.middleware,
        block_ip.KeyShield(TELEGRAM_API_KEY).middleware,
        initilize_session.middleware,
    ])
    app.router.add_post("/mogiminsk/tg/", telegram_webhook)
    app.on_startup.append(init_client)
    app.on_cleanup.append(destroy_client)
    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(init(sys.argv), host='127.0.0.1', port=8090)
