import argparse
import asyncio
import logging.config

from aiohttp import web

from aiohttp_translation import activate, gettext as _
from bot_telegram.utils.telegram_states import get_state
from bot_telegram.utils.telegram_api import Update, get_or_create_user, TgSender
from mogiminsk.utils import init_client, destroy_client
from mogiminsk.middleware import (
    block_ip,
    initilize_session,
    suppress_error,
    clear_tasklocal,
)
from mogiminsk.settings import TELEGRAM_API_KEY, LOGGING, LANGUAGE

logger = logging.getLogger(__name__)


async def telegram_webhook(request):
    data = await request.json()
    logger.info(f'Request:\n{data}')
    update = Update.create(data)
    request['user'] = get_or_create_user(request['db'], update.get_user())
    activate(request['user'].language or LANGUAGE)
    if not (update.message or update.callback_query):
        raise ValueError('Got unexpected message type: {}'.format(update))

    state = get_state(request['user'])

    try:
        bot_messages = await state.consume(update.get_common_message())
    except Exception as e:
        logger.exception(e)
        request['user'].telegram_context = {'state': 'where'}
        bot_messages = \
            get_state(request['user']).get_intro_message().to_sequence([
                _('Something went wrong...')
            ])

    if bot_messages:
        request['db'].commit()
        connector = TgSender(update.get_chat().id, request.app['client'], request['user'])
        asyncio.ensure_future(
            connector.send_messages(
                bot_messages, update.get_message().id if update.callback_query else None
            )
        )

    if update.callback_query:
        return web.json_response({
            'method': 'answerCallbackQuery',
            'callback_query_id': update.callback_query.id,
        })

    return web.Response()


def init():
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    parser.add_argument('--port')    

    args = parser.parse_args()
    port = args.port

    if port:
        port = int(port)

    elif not args.path:
        port = 8090

    if port:
        web.run_app(init(), host='0.0.0.0', port=port)

    else:
        web.run_app(init(), path=args.path, port=None)

    

