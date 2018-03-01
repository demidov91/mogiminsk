import logging
from typing import Iterable

from aiohttp_translation import activate, default_language as aiohttp_default_language

from messager.input_data import InputMessage, InputContact
from mogiminsk.models import User
from mogiminsk.services import UserService
from mogiminsk.settings import VIBER_TOKEN, LANGUAGE
from messager.helper import OptionalObjectFactoryMixin
from bot.messages.base import BotMessage
from bot_viber import defines
from bot_viber.defines import VIBER_BOT
from bot_viber.utils.viber_messages import to_viber_message


SEND_URL = 'https://chatapi.viber.com/pa/send_message'
API_URL = 'https://chatapi.viber.com/pa/'

logger = logging.getLogger(__name__)


class Update(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.event = data['event']
        self.message = Message.create(data.get('message'))
        self.user = ViberUser.create(data.get('sender') or data.get('user'))
        self.description = data.get('desc')

        if self.user is None and 'user_id' in data:
            self.user = ViberUser({'id': data['user_id']})

    def is_system_update(self):
        return self.event != defines.EVENT_TYPE_MESSAGE


class Message(OptionalObjectFactoryMixin):
    @classmethod
    def create(cls, data):
        if not data or data.get('type') not in ('text', 'contact'):
            return None

        return super().create(data)

    def __init__(self, data):
        self.text = data.get('text')
        self.contact = ViberContact.create(data.get('contact'))


class ViberUser(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name')
        self.language = data.get('language')

    def get_bot_language(self):
        if self.language in (aiohttp_default_language, LANGUAGE):
            return self.language

        return LANGUAGE


class ViberContact(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.phone_number = data['phone_number']
        self.name = data.get('name')
        self.avatar = data.get('avatar')

    def is_user_contact(self):
        return self.name is None


def to_input_message(viber_update: Update) ->InputMessage:
    text = viber_update.message and viber_update.message.text
    contact = None

    if viber_update.message and viber_update.message.contact:
        contact = InputContact(
            phone=viber_update.message.contact.phone_number,
            is_user_phone=viber_update.message.contact.is_user_contact()
        )

    return InputMessage(text=text, data=text, contact=contact)


class ViberSender:
    SEND_MESSAGE = 'send_message'
    SET_WEBHOOK = 'set_webhook'
    GET_ACCOUNT_INFO = 'get_account_info'

    def __init__(self, client):
        self.client = client

    async def send_messages(self, receiver: ViberUser, messages: Iterable[BotMessage]):
        activate(receiver.language)
        for bot_message in messages:
            await self.post_data(
                self.SEND_MESSAGE,
                to_viber_message(bot_message, receiver)
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
            logger.info(
                'Got following response from the viber server (%s):\n%s',
                response.status,
                (await response.read())
            )

            if response.status != 200:
                raise ValueError(f'Status is {response.status} instead of 200.')

            response_data = await response.json()
            if response_data.get('status') != 0:
                logger.warning(
                    'Unexpected Viber server response. 0 expected, got %s. Status message is: %s',
                    response_data.get('status'),
                    response_data.get('status_message')
                )
                raise ValueError(f'Error Viber server response:\n{response_data}')


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
            viber_context={
                'state': 'initial',
                'bot': VIBER_BOT,
            },
            viber_id=remote_user.id,
            language=remote_user.get_bot_language(),
        )

    return user
