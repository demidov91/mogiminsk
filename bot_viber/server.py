import asyncio
import json
import logging
from typing import Iterable

from aiohttp import web
from sqlalchemy.orm.attributes import flag_modified

from block_ip.decorators import api_key
from bot.messages.base import BotMessage
from bot_viber.utils.viber_api import (
    get_or_create_user,
    get_viber_user,
    to_input_message,
    Update,
    ViberSender
)
from mogiminsk.services.user import UserService
from mogiminsk.settings import VIBER_API_KEY
from mogiminsk.utils import Session, set_db, get_db
from messager.bot_server import BotServer


logger = logging.getLogger(__name__)


class ViberServer(BotServer):
    @classmethod
    @api_key(VIBER_API_KEY)
    async def webhook(cls, request):
        return await super().webhook(request)

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
        return to_input_message(remote_update)

    @classmethod
    def get_or_create_user(cls, remote_update):
        return get_or_create_user(get_viber_user(remote_update))

    @classmethod
    async def send_the_answer(cls,
                              request,
                              remote_update: Update,
                              bot_messages: Iterable[BotMessage]):
        if not bot_messages:
            return

        request['db'].commit()
        asyncio.ensure_future(
            cls._answer_callback(request.app['client'], remote_update.user, bot_messages)
        )

    @classmethod
    async def _answer_callback(cls, client, remote_user, bot_messages):
        sender = ViberSender(client)
        try:
            await sender.send_messages(remote_user, bot_messages)
        except:
            logger.exception('Got exception during sending message to Viber server. Messages:\n%s',
                             bot_messages)

            set_db(Session())
            try:
                user = UserService.get_by_viber_id(remote_user.id)
                messages = cls.handle_exception(user)
                get_db().commit()
                await sender.send_messages(remote_user, messages)
            except:
                logger.exception("Couldn't even reset the state.")

            finally:
                get_db().close()

    @classmethod
    def get_response(cls, update):
        return web.Response()

    @classmethod
    async def handle_no_user_update(cls, remote_update):
        logger.info('Got no-user update: %s', remote_update)
        return web.Response()

    @classmethod
    def save_data(cls, state):
        super().save_data(state)
        state.user.viber_context = state.data
        flag_modified(state.user, 'viber_context')
