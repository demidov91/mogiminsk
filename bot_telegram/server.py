import asyncio
import logging

from aiohttp import web

from bot_telegram.middleware import error_handler_middleware, session_initializer_middleware
from bot_telegram.utils.states_helper import get_state, ERROR_MESSAGE
from bot_telegram.utils.telegram_helper import Update, get_api_url, get_db_user
from mogiminsk.utils import init_client, destroy_client, init_db, close_db

logger = logging.getLogger(__name__)


async def telegram_webhook(request):
    data = await request.json()
    update = Update.create(data)
    request['user'] = get_db_user(request['db'], update.get_user())
    if not (update.message or update.callback_query):
        raise ValueError('Got unexpected message type: {}'.format(update))

    state = get_state(update, request)

    try:
        state.consume(update.get_text())
        bot_message = state.produce()
    except Exception as e:
        logger.exception(e)
        bot_message = ERROR_MESSAGE
        state.data = {'state': 'where'}

    response_data = bot_message.to_telegram_data(state.data)

    if update.callback_query and bot_message.buttons:
        response_data.update({
            'method': 'editMessageText',
            'chat_id': update.get_chat().id,
            'message_id': update.get_message().id,
        })

    else:
        response_data.update({
            'method': 'sendMessage',
            'chat_id': update.get_chat().id,
        })

    asyncio.ensure_future(post_data(response_data, request.app['client']))

    if update.callback_query:
        return web.json_response({
            'method': 'answerCallbackQuery',
            'callback_query_id': update.callback_query.id,
        })

    return web.Response()

async def post_data(request_to_tg_server: dict, client):
    url = get_api_url(request_to_tg_server.pop('method'))

    async with client.post(url, json=request_to_tg_server) as response:
        if response.status != 200:
            logger.error('Got unexpected tg server response status: %s. Content: %s',
                         response.satus, (await response.read()))
            return

        try:
            response_data = await response.json()
            if not response_data['ok']:
                logger.error("tg responded with ok != True. Response data: %s", response_data)
        except:
            logger.exception("Can't parse server response.")


def init(argv):
    app = web.Application(middlewares=[
        session_initializer_middleware,
        error_handler_middleware,
    ])
    app.router.add_post("/mogiminsk/tg/", telegram_webhook)
    app.on_startup.append(init_db)
    app.on_startup.append(init_client)
    app.on_cleanup.append(destroy_client)
    app.on_cleanup.append(close_db)
    return app


if __name__ == '__main__':
    import sys
    web.run_app(init(sys.argv), host='127.0.0.1', port=8090)
