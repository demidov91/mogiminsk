from .base import BaseService
from mogiminsk.models import Conversation, User


class ConversationService(BaseService):
    model = Conversation

    @classmethod
    def add_user_message(cls,
                         user: User,
                         text: str,
                         context: dict,
                         messenger: str) ->Conversation:
        return cls.add(
            user=user,
            text=text,
            messenger=messenger,
            context=context,
            is_user_message=True
        )

    @classmethod
    def add_bot_message(cls, user: User, text: str, messenger:str) ->Conversation:
        return cls.add(user=user, text=text, messenger=messenger, is_user_message=False)

    @classmethod
    def not_seen(cls):
        return cls.query().filter(Conversation.seen == False)
