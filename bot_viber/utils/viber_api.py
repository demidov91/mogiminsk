import logging
from typing import Iterable

from messager.input_data import InputMessage
from mogiminsk.models import User
from mogiminsk.services import UserService
from mogiminsk.settings import VIBER_TOKEN
from messager.helper import OptionalObjectFactoryMixin
from bot.messages.base import BotMessage


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


class ViberSender:
    SEND_MESSAGE = 'send_message'
    SET_WEBHOOK = 'set_webhook'
    GET_ACCOUNT_INFO = 'get_account_info'

    def __init__(self, client):
        self.client = client

    @classmethod
    def build_informative_message(cls, bot_message: BotMessage) ->dict:
        return {
            'text': bot_message.text,
            'type': 'text',
        }

    @classmethod
    def build_full_message(cls, bot_message: BotMessage, receiver: ViberUser):
        informative_message = cls.build_informative_message(bot_message)
        informative_message['receiver'] = receiver.id
        return informative_message

    async def send_messages(self, receiver: ViberUser, messages: Iterable[BotMessage]):
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
            viber_id=remote_user.id
        )

    return user
