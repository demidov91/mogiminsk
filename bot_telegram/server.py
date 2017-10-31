import asyncio
import logging

from aiohttp import web

from aiohttp_translation import activate, gettext as _
from bot.state_lib.mediator import get_state_class
from bot_telegram.utils.telegram_api import Update, get_or_create_user, TgSender

from mogiminsk.settings import LANGUAGE

logger = logging.getLogger(__name__)


class TgServer:
    @classmethod
    def get_bot_context(cls, user):
        return user.telegram_context

    @classmethod
    def set_bot_context(cls, user, full_context: dict):
        user.telegram_context = full_context

    @classmethod
    def get_state(cls, user):
        state_name = cls.get_bot_context(user).get('state')
        return get_state_class(state_name)(user)

    @classmethod
    async def get_remote_update(cls, request):
        data = await  request.json()
        logger.info(f'Request:\n{data}')
        update = Update.create(data)

        if not (update.message or update.callback_query):
            raise ValueError('Got unexpected message type: {}'.format(update))

        return update

    @classmethod
    def get_or_create_user(cls, remote_update):
        return get_or_create_user(remote_update.get_user())

    @classmethod
    async def consume(cls, user, state, common_message):
        try:
            return await state.consume(common_message)
        except Exception as e:
            logger.exception(e)
            cls.set_bot_context(user, {'state': 'where'})
            return cls.get_state(user).get_intro_message().to_sequence([
                _('Something went wrong...')
            ])

    @classmethod
    async def send_the_answer(cls, request, update, bot_messages):
        if bot_messages:
            request['db'].commit()
            connector = TgSender(update.get_chat().id, request.app['client'], request['user'])
            asyncio.ensure_future(
                connector.send_messages(
                    bot_messages, update.get_message().id if update.callback_query else None
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

    @classmethod
    async def webhook(cls, request):
        remote_update = await cls.get_remote_update(request)
        request['user'] = cls.get_or_create_user(remote_update)
        activate(request['user'].language or LANGUAGE)

        state = cls.get_state(request['user'])
        common_message = remote_update.get_common_message()

        bot_messages = await cls.consume(request['user'], state, common_message)

        await cls.send_the_answer(request, remote_update, bot_messages)

        return cls.get_response(remote_update)
