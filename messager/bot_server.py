import logging
from typing import Iterable

from aiohttp_translation import activate, gettext_lazy as _
from sqlalchemy.orm.attributes import flag_modified

from bot.messages.base import BotMessage
from bot.state_lib.mediator import get_state_class
from bot.state_lib.base import BaseState
from messager.input_data import InputMessage
from mogiminsk.models import User
from mogiminsk.settings import LANGUAGE


logger = logging.getLogger(__name__)


class BotServer:
    @classmethod
    def get_state(cls, user: User) ->BaseState:
        context = cls.get_bot_context(user)
        state_name = context.get('state')
        return get_state_class(state_name)(user, context)

    @classmethod
    async def consume(
            cls,
            user: User,
            state: BaseState,
            common_message: InputMessage) ->Iterable[BotMessage]:
        try:
            messages = await state.consume(common_message)
            cls.save_data(state)
            return messages
        except Exception as e:
            logger.exception(e)
            return cls.handle_exception(user)

    @classmethod
    async def webhook(cls, request):
        remote_update = await cls.get_remote_update(request)
        request['user'] = cls.get_or_create_user(remote_update)
        activate(request['user'].language if request['user'] is not None else LANGUAGE)

        if remote_update.is_system_update():
            return await cls.handle_system_message(remote_update)

        if request['user'] is None:
            raise ValueError("User can't be None.")

        state = cls.get_state(request['user'])
        common_message = cls.get_input_message(remote_update)

        bot_messages = await cls.consume(request['user'], state, common_message)

        await cls.send_the_answer(request, remote_update, bot_messages)

        return cls.get_response(remote_update)

    @classmethod
    def handle_exception(cls, user: User) ->Iterable[BotMessage]:
        cls.set_bot_context(user, {'state': 'where'})
        return cls.get_state(user).get_intro_message().to_sequence([
            _('Something went wrong...')
        ])

    @classmethod
    def get_bot_context(cls, user):
        raise NotImplementedError()

    @classmethod
    def set_bot_context(cls, user, full_context: dict):
        raise NotImplementedError()

    @classmethod
    async def get_remote_update(cls, request):
        raise NotImplementedError()

    @classmethod
    def get_input_message(cls, remote_update) ->InputMessage:
        raise NotImplementedError

    @classmethod
    def get_or_create_user(cls, remote_update) -> User:
        raise NotImplementedError()

    @classmethod
    async def send_the_answer(cls,
                              request,
                              remote_update,
                              bot_messages: Iterable[BotMessage]):
        raise NotImplementedError()

    @classmethod
    def get_response(cls, remote_update):
        raise NotImplementedError()

    @classmethod
    async def handle_system_message(cls, remote_update):
        raise NotImplementedError()

    @classmethod
    def save_data(cls, state: BaseState):
        flag_modified(state.user, 'external')
