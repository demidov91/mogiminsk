import logging
from typing import Iterable

from aiohttp_translation import activate, default_language as aiohttp_default_language

from messager.input_data import InputMessage
from mogiminsk.models import User
from mogiminsk.services import UserService
from mogiminsk.settings import VIBER_TOKEN, LANGUAGE
from messager.helper import OptionalObjectFactoryMixin
from bot.messages.base import BotMessage
from bot_viber.constants import VIBER_BUTTONS_WIDTH


BOT_NAME = 'Vasja'
SEND_URL = 'https://chatapi.viber.com/pa/send_message'
API_URL = 'https://chatapi.viber.com/pa/'


class Update(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.event = data['event']
        self.message = Message.create(data.get('message'))
        self.user = ViberUser(data['sender'])


class Message(OptionalObjectFactoryMixin):
    @classmethod
    def create(cls, data):
        if data.get('type') != 'text':
            return None

        return super().create(data)

    def __init__(self, data):
        self.text = data.get('text')


class ViberUser(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name')
        self.language = data.get('language')

    def get_bot_language(self):
        if self.language in (aiohttp_default_language, LANGUAGE):
            return self.language

        return LANGUAGE


def build_basic_message(bot_message: BotMessage) ->dict:
    return {
        'text': bot_message.text,
        'type': 'text',
    }


def add_keyboard_into_message(viber_message: dict, bot_message: BotMessage):
    buttons = []
    for row in bot_message.buttons:
        viber_width = VIBER_BUTTONS_WIDTH // len(row)

        for bot_button in row:
            buttons.append({
                'Columns': viber_width,
                'ActionType': 'reply',
                'ActionBody': bot_button['data'],
                'Text': bot_button['text'],
            })

    viber_message['keyboard'] = {
        'Type': 'keyboard',
        'Buttons': buttons,
    }


class ViberSender:
    SEND_MESSAGE = 'send_message'
    SET_WEBHOOK = 'set_webhook'
    GET_ACCOUNT_INFO = 'get_account_info'

    def __init__(self, client):
        self.client = client

    @classmethod
    def build_full_message(cls, bot_message: BotMessage, receiver: ViberUser):
        viber_message = build_basic_message(bot_message)
        if bot_message.buttons:
            add_keyboard_into_message(viber_message, bot_message)

        viber_message['receiver'] = receiver.id
        return viber_message

    async def send_messages(self, receiver: ViberUser, messages: Iterable[BotMessage]):
        activate(receiver.language)
        for bot_message in messages:
            await self.post_data(
                self.SEND_MESSAGE,
                self.build_full_message(bot_message, receiver)
            )

    async def post_data(self, action: str, data: dict):
        url = API_URL + action
        logging.info('Following message will be sent to %s:\n%s', url, data)
        async with self.client.post(
                url,
                json=data,
                headers={
                    'X-Viber-Auth-Token': VIBER_TOKEN,
                    'Content-Type': 'application/json',
                }) as response:
            logging.info(
                'Got following response from the viber server (%s):\n%s',
                response.status,
                (await response.read())
            )


def get_input_message(update: dict) ->InputMessage:
    return Update.create(update)


def get_viber_user(update: Update) ->ViberUser:
    return update.user


def get_db_user(remote_user: ViberUser) -> User:
    return UserService.filter_by(viber_id=remote_user.id).first()


def get_or_create_user(remote_user: ViberUser):
    if remote_user is None:
        return None

    user = get_db_user(remote_user)
    if user is None:
        user = UserService.add(
            viber_context={'state': 'initial'},
            viber_id=remote_user.id,
            language=remote_user.get_bot_language(),
        )

    return user
