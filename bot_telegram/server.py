import asyncio
import logging

from aiohttp import web

from bot_telegram.utils.telegram_api import Update, get_or_create_user, TgSender
from messager.bot_server import BotServer

logger = logging.getLogger(__name__)


class TgServer(BotServer):
    @classmethod
    def get_bot_context(cls, user):
        return user.telegram_context

    @classmethod
    def set_bot_context(cls, user, full_context: dict):
        user.telegram_context = full_context

    @classmethod
    async def get_remote_update(cls, request):
        data = await  request.json()
        logger.info(f'Request:\n{data}')
        update = Update.create(data)

        if not (update.message or update.callback_query):
            raise ValueError('Got unexpected message type: {}'.format(update))

        return update

    @classmethod
    def get_input_message(cls, remote_update):
        return remote_update.get_input_message()

    @classmethod
    def get_or_create_user(cls, remote_update):
        return get_or_create_user(remote_update.get_user())

    @classmethod
    async def send_the_answer(cls, request, remote_update, bot_messages):
        if not bot_messages:
            return

        request['db'].commit()
        connector = TgSender(remote_update.get_chat().id, request.app['client'], request['user'])
        asyncio.ensure_future(
            connector.send_messages(
                bot_messages, remote_update.get_message().id if remote_update.callback_query else None
            )
        )

    @classmethod
    def get_response(cls, update):
        if update.callback_query:
            return web.json_response({
                'method': 'answerCallbackQuery',
                'callback_query_id': update.callback_query.id,
            })

        return web.Response()
