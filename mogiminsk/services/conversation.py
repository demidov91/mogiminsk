from .base import BaseService
from mogiminsk.models import Conversation, User


class ConversationService(BaseService):
    model = Conversation

    @classmethod
    def add_user_message(cls, user: User, text: str) ->Conversation:
        return cls.add(user=user, text=text, is_user_message=True)

    @classmethod
    def add_bot_message(cls, user: User, text: str) ->Conversation:
        return cls.add(user=user, text=text, is_user_message=False)
