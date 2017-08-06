from mogiminsk.settings import TELEGRAM_TOKEN
from mogiminsk.models import User
from sqlalchemy.orm import Session
from typing import TypeVar, Type
from urllib.parse import parse_qsl

C = TypeVar('C')


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


class Chat(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = int(data['id'])


class CallbackQuery(OptionalObjectFactoryMixin):
    def __init__(self, data):
        self.id = data['id']
        self.user = TelegramUser.create(data['from'])
        self.message = Message.create(data.get('message'))
        self.data = data.get('data')


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


def get_api_url(method: str):
    return f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}'


def get_db_user(db: Session, remote_user: TelegramUser) -> User:
    return db.query(User).filter(User.telegram_id == remote_user.id).first()


def get_or_create_user(db: Session, remote_user: TelegramUser):
    user = get_db_user(db, remote_user)
    if user is None:
        user = User(telegram_context={'state': 'initial'}, telegram_id=remote_user.id)
        db.add(user)

    return user
