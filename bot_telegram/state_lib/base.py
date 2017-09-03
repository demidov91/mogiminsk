from typing import Dict, Type

from sqlalchemy.orm.attributes import flag_modified

from bot_telegram.messages import BotMessage

STATES = {}     # type: Dict[str, Type[BaseState]]


class BaseState:
    _intro_message = None    # type: BotMessage
    message_was_not_recognized = False
    is_callback_state = True
    value = None
    text = None
    contact = None

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()[:-5]

    def __init_subclass__(cls, **kwargs):
        super(BaseState, cls).__init_subclass__()
        STATES[cls.get_name()] = cls

    def __init__(self, user):
        self.data = user.telegram_context
        self.user = user

    def get_intro_message(self):
        return self._intro_message

    def get_state(self) -> str:
        return self.data['state']

    def set_state(self, state_name: str):
        self.data['state'] = state_name

    def consume(self, common_message):
        self.value = common_message.data
        self.data[self.get_name()] = self.value
        self.text = common_message.text
        self.contact = common_message.contact

        if self.value == 'back':
            self.set_state(self.pop_history())
            return

        self.process()

    def process(self):
        """
        Updates user state and sets *is_unrecognized* value.
        """
        raise NotImplementedError()

    def produce(self) ->BotMessage:
        self.save_data()
        next_state = STATES[self.get_state()](self.user)
        message = next_state.get_intro_message()
        if self.message_was_not_recognized:
            return message.get_error_message()

        return message

    def save_data(self):
        self.append_history(self.get_state())
        self.user.telegram_context = self.data
        flag_modified(self.user, 'telegram_context')

    def pop_history(self):
        history = self.data.get('history')
        if history:
            history.pop()
            if history:
                return history.pop()

        return 'where'

    def back_to(self, state):
        history = self.data.get('history', [])
        last_popped = None
        while history and last_popped != state:
            last_popped = history.pop()

        return last_popped or 'where'

    def append_history(self, state):
        history = self.data.get('history', [])
        history.append(state)
        self.data['history'] = history
