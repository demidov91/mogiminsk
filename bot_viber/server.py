import logging

from aiohttp import web

from messager.bot_server import BotServer
from bot_viber.utils.viber_api import get_input_message, get_or_create_user, get_viber_user


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
        data = await request.post()
        logger.debug('Got viber update: %s', data)
        return request.app['viber'].parse_request(data)

    @classmethod
    def get_input_message(cls, remote_update):
        return get_input_message(remote_update)

    @classmethod
    def get_or_create_user(cls, remote_update):
        return get_or_create_user(get_viber_user(remote_update))

    @classmethod
    async def send_the_answer(cls, request, update, bot_messages):
        pass

    @classmethod
    def get_response(cls, update):
        return web.Response()