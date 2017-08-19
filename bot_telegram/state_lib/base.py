from typing import Dict, Type

from sqlalchemy.orm.attributes import flag_modified

from bot_telegram.messages import BotMessage

STATES = {}     # type: Dict[str, Type[BaseState]]


class BaseState:
    _intro_message = None    # type: BotMessage
    message_was_not_recognized = False
    is_callback_state = True

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()[:-5]

    def __init_subclass__(cls, **kwargs):
        super(BaseState, cls).__init_subclass__()
        STATES[cls.get_name()] = cls

    def __init__(self, value, user):
        self.data = user.telegram_context
        self.value = value
        self.data[self.get_name()] = self.value
        self.user = user

    @classmethod
    def get_intro_message(cls, data):
        return cls._intro_message

    def get_state(self) -> str:
        return self.data['state']

    def set_state(self, state_name: str):
        self.data['state'] = state_name

    def consume(self, text: str):
        """
        Updates user state and sets *is_unrecognized* value.
        """
        raise NotImplementedError()

    def produce(self) ->BotMessage:
        self.save_data()
        next_state_class = STATES[self.get_state()]
        message = next_state_class.get_intro_message(self.data)
        if self.message_was_not_recognized:
            return message.get_error_message()

        return message

    def save_data(self):
        self.user.telegram_context = self.data
        flag_modified(self.user, 'telegram_context')
