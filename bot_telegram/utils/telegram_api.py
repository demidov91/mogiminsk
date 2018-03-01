import asyncio
import re
import logging

from aiohttp_translation import activate
from bot_telegram.utils.telegram_messages import TextButtonFormatter, InlineButtonFormatter
from bot.messages.base import BotMessage
from bot_telegram.defines import TELEGRAM_BOT
from mogiminsk.settings import TELEGRAM_TOKEN, LANGUAGE
from mogiminsk.models import User
from mogiminsk.services import UserService
from mogiminsk.utils import Session
from messager.input_data import InputMessage, InputContact
from messager.helper import OptionalObjectFactoryMixin


logger = logging.getLogger(__name__)


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
    # Phone number without leading '+'
    phone_pattern = re.compile('(?P<number>\d+)')

    def __init__(self, data):
        number_match = self.phone_pattern.search(data['phone_number'])        
        self.phone = number_match.group('number')
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

    def get_input_message(self) ->InputMessage:
        data = self.get_data()
        text = self.get_text()
        contact = self.get_contact()
        user_id = self.get_message().user.id

        if contact is None:
            tg_contact = None

        else:
            tg_contact = InputContact(
                phone=contact.phone, is_user_phone=contact.user_id == user_id
            )

        return InputMessage(data=data, text=text, contact=tg_contact)

    def is_system_update(self):
        return False


def to_telegram_message(message: BotMessage, chat_id):
    formatted = {
        'text': message.text,
        'method': 'sendMessage',
        'chat_id': chat_id,
    }

    if message.parse_mode:
        formatted['parse_mode'] = message.parse_mode

    buttons = message.get_tg_buttons()

    if buttons:

        if message.is_tg_text_buttons:
            formatted['reply_markup'] = {
                'keyboard': TextButtonFormatter.format_list(buttons),
                'resize_keyboard': True,
                'one_time_keyboard': True,
            }

        else:
            formatted['reply_markup'] = {
                'inline_keyboard': InlineButtonFormatter.format_list(buttons),
            }

    return formatted


class TgSender:
    def __init__(self, chat_id: int, client, user: User):
        self.db_session = Session(autocommit=True)
        self.chat_id = chat_id
        self.client = client
        self.user = self.db_session.query(User).get(user.id)
        self._loop = asyncio.get_event_loop()

    async def send_messages(self, messages: list, callback_message_id: int):
        activate(self.user.language)
        converted_messages = tuple(to_telegram_message(x, self.chat_id) for x in messages)

        if callback_message_id is not None and not messages[0].is_tg_text_buttons:
            converted_messages[0].update({
                'method': 'editMessageText',
                'message_id': callback_message_id,
            })

        just_sent_messages = []
        for msg in converted_messages:
            response_data = await self.post_data(msg)
            if response_data is not None and 'result' in response_data and 'message_id' in response_data['result']:
                just_sent_messages.append(response_data['result']['message_id'])

        await self.remove_previous_messages(dont_touch=(callback_message_id, ))
        await self.save_current_messages(just_sent_messages)

    async def remove_previous_messages(self, dont_touch=()):
        prev_messages = set(int(x) for x in self.user.telegram_messages.split(',') if x)
        prev_messages -= set(dont_touch)
        await asyncio.gather(*(
            self.post_data({
                'method': 'deleteMessage',
                'chat_id': self.chat_id,
                'message_id': x
            }) for x in prev_messages)
        )

    async def save_current_messages(self, messages_id):
        self.db_session.query(User).update({
            User.telegram_messages: ','.join(str(x) for x in messages_id)
        })

    async def post_data(self, request_to_tg_server: dict):
        url = self.get_api_url(request_to_tg_server.pop('method'))
        logger.info(f'Response ({url}):\n{request_to_tg_server}')

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


def get_db_user(remote_user: TelegramUser) -> User:
    return UserService.filter_by(telegram_id=remote_user.id).first()


def get_or_create_user(remote_user: TelegramUser):
    user = get_db_user(remote_user)
    if user is None:
        user = UserService.add(
            telegram_context={
                'state': 'initial',
                'bot': TELEGRAM_BOT,
            },
            telegram_id=remote_user.id,
            language=LANGUAGE,
        )

    return user
