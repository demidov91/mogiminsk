import asyncio
from typing import TypeVar, Type
import logging

from bot_telegram.utils.messages_helper import TextButtonFormatter, InlineButtonFormatter
from bot_telegram.messages import BotMessage
from mogiminsk.settings import TELEGRAM_TOKEN
from mogiminsk.models import User
from mogiminsk.utils import Session
from messager.input_data import Message as CommonMessage, Contact as CommonContact


C = TypeVar('C')
logger = logging.getLogger(__name__)


class OptionalObjectFactoryMixin:
    @classmethod
    def create(cls: Type[C], data) -> C:
        if data is None:
            return

        return cls(data)


class TelegramUser(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = int(data['id'])
        self.username = data.get('username')


class Message(OptionalObjectFactoryMixin):
    def __init__(self, data: dict):
        self.id = int(data['message_id'])
        self.user = TelegramUser.create(data.get('from'))
        self.text = data.get('text')
        self.chat = Chat(data['chat'])
        self.contact = Contact.create(data.get('contact'))


class Chat(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = int(data['id'])


class CallbackQuery(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = data['id']
        self.user = TelegramUser.create(data['from'])
        self.message = Message.create(data.get('message'))
        self.data = data.get('data')


class Contact(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.phone = data['phone_number']
        self.user_id = data.get('user_id')


class Update(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.update_id = int(data['update_id'])
        self.message = Message.create(data.get('message'))
        self.callback_query = CallbackQuery.create(data.get('callback_query'))

    def get_data(self):
        if self.callback_query is None:
            return

        return self.callback_query.data

    def get_text(self):
        return self.message and self.message.text

    def get_user(self):
        if self.callback_query:
            return self.callback_query.user

        if self.message:
            return self.message.user

        return None

    def get_message(self):
        if self.message:
            return self.message

        if self.callback_query:
            return self.callback_query.message

    def get_chat(self):
        message = self.get_message()
        return message and message.chat

    def get_contact(self):
        msg = self.get_message()
        if not msg:
            return

        return msg.contact

    def get_common_message(self):
        data = self.get_data()
        text = self.get_text()
        contact = self.get_contact()
        if contact is not None:
            contact = CommonContact(
                phone=contact.phone, identifier=contact.user_id
            )

        return CommonMessage(data=data, text=text, contact=contact)


class TgSender:
    def __init__(self, chat_id: int, client, user: User):
        self.db_session = Session(autocommit=True)
        self.chat_id = chat_id
        self.client = client
        self.user = self.db_session.query(User).get(user.id)
        self._loop = asyncio.get_event_loop()

    def convert_message(self, message):
        msg = self.to_telegram_message(message)
        msg.update({
            'method': 'sendMessage',
            'chat_id': self.chat_id,
        })
        return msg

    async def send_messages(self, messages):
        converted_messages = tuple(self.convert_message(x) for x in messages)
        current_messages = set()
        for msg in converted_messages:
            response_data = await self.post_data(msg)
            if response_data is not None and 'result' in response_data and 'message_id' in response_data['result']:
                current_messages.add(response_data['result']['message_id'])

        current_messages.update(await self.remove_previous_messages())
        await self.save_current_messages(current_messages)

    async def remove_previous_messages(self):
        prev_messages = tuple(int(x) for x in self.user.telegram_messages.split(',') if x)
        for response_data in await asyncio.gather(*(
            self.post_data({
                'method': 'deleteMessage',
                'chat_id': self.chat_id,
                'message_id': x
            }) for x in prev_messages)
        ):
            if response_data is not None:
                logger.info(response_data)

        return []

    async def save_current_messages(self, messages_id):
        self.db_session.query(User).update({
            User.telegram_messages: ','.join(str(x) for x in messages_id)
        })

    async def post_data(self, request_to_tg_server: dict):
        url = self.get_api_url(request_to_tg_server.pop('method'))

        async with self.client.post(url, json=request_to_tg_server) as response:
            if response.status != 200:
                logger.error('Got unexpected tg server response status: %s.\n'
                             'Request: %s.\n'
                             'Response: %s',
                             response.status,
                             request_to_tg_server,
                             (await response.read())
                             )
                return

            try:
                response_data = await response.json()
                if not response_data['ok']:
                    logger.error("tg responded with ok != True. Request: %s.\n"
                                 "Response data: %s", request_to_tg_server, response_data)
            except:
                logger.exception("Can't parse server response. Request was: %s", request_to_tg_server)
                return

            return response_data

    @staticmethod
    def get_api_url(method: str):
        return f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}'

    @staticmethod
    def to_telegram_message(message: BotMessage):
        formatted = {
            'text': message.text,
        }

        if message.parse_mode:
            formatted['parse_mode'] = message.parse_mode

        if message.text_buttons:
            formatted['reply_markup'] = {
                'keyboard': TextButtonFormatter.format_list(message.text_buttons),
                'resize_keyboard': True,
                'one_time_keyboard': True,
            }

        elif message.buttons:
            formatted['reply_markup'] = {
                'inline_keyboard': InlineButtonFormatter.format_list(message.buttons),
            }

        return formatted


def get_db_user(db: Session, remote_user: TelegramUser) -> User:
    return db.query(User).filter(User.telegram_id == remote_user.id).first()


def get_or_create_user(db: Session, remote_user: TelegramUser):
    user = get_db_user(db, remote_user)
    if user is None:
        user = User(telegram_context={'state': 'initial'}, telegram_id=remote_user.id)
        db.add(user)

    return user



