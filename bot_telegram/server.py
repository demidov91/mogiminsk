from aiohttp import web
import logging
from bot_telegram.util import Update, get_api_url, get_db_user
from bot_telegram.states import get_state, ERROR_MESSAGE
from bot_telegram.middleware import error_handler_middleware, session_initializer_middleware
from mogiminsk.utils import init_client, destroy_client, init_db, close_db
import asyncio

logger = logging.getLogger(__name__)


async def telegram_webhook(request):
    data = await request.json()
    update = Update.create(data)
    request['user'] = get_db_user(request['db'], update.get_user())
    if update.message or update.callback_query:
        state = get_state(update.get_data(), request)
        try:
            state.consume(update.get_text())
            bot_message = state.produce()
        except Exception as e:
            logger.exception(e)
            bot_message = ERROR_MESSAGE
            state.data = {'state': 'where'}

        response_data = bot_message.to_telegram_data(state.data)

        if update.callback_query:
            asyncio.ensure_future(request.app['client'].post(
                get_api_url('answerCallbackQuery'),
                json={
                    'callback_query_id': update.callback_query.id,
                }
            ))
            response_data.update({
                'method': 'editMessageText',
                'chat_id': update.callback_query.message.chat.id,
                'message_id': update.callback_query.message.id,
            })
        else:
            response_data.update({
                'method': 'sendMessage',
                'chat_id': update.message.chat.id,
            })

        return web.json_response(response_data)

    return web.Response()


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
