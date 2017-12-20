import asyncio
import json
import logging
from typing import Iterable

from aiohttp import web

from bot.messages.base import BotMessage
from bot_viber.utils.viber_api import (
    get_or_create_user,
    get_viber_user,
    Update,
    ViberSender
)
from messager.bot_server import BotServer
from messager.input_data import InputMessage


logger = logging.getLogger(__name__)


class ViberServer(BotServer):
    @classmethod
    def get_bot_context(cls, user):
        return user.viber_context

    @classmethod
    def set_bot_context(cls, user, full_context: dict):
        user.viber_context = full_context

    @classmethod
    async def get_remote_update(cls, request):
        data = await request.read()
        logger.debug('Got viber update: %s', data)
        remote_update = json.loads(data)

        if remote_update.get('event') != 'message':
            logger.warning('Unexpected event: %s.', remote_update.get('event'))
            return None

        return Update.create(remote_update)

    @classmethod
    def get_input_message(cls, remote_update: Update):
        return InputMessage(
            text=remote_update.message.text,
            data=remote_update.message.text
        )

    @classmethod
    def get_or_create_user(cls, remote_update):
        return get_or_create_user(get_viber_user(remote_update))

    @classmethod
    async def send_the_answer(cls,
                              request,
                              remote_update: Update,
                              bot_messages: Iterable[BotMessage]):
        sender = ViberSender(request.app['client'])
        asyncio.ensure_future(sender.send_messages(remote_update.user, bot_messages))

    @classmethod
    def get_response(cls, update):
        return web.Response()

    @classmethod
    async def handle_no_user_update(cls, remote_update):
        logger.info('Got no-user update: %s', remote_update)
        return web.Response()