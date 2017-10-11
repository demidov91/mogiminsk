import logging
from typing import Dict, Type, Sequence

from sqlalchemy.orm.attributes import flag_modified

from bot_telegram.messages import BotMessage


logger = logging.getLogger(__name__)
STATES = {}     # type: Dict[str, Type[BaseState]]


class BaseState:
    """
    Reserved *data* keys:
        **state** - current state name.
        **messages** - messages to show a user. Should be shown once before main message.
    """

    _intro_message = None    # type: BotMessage
    message_was_not_recognized = False
    is_callback_state = True
    value = None
    text = None
    contact = None
    ignorable_values = '-',
    back = None

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()[:-5]

    def __init_subclass__(cls, **kwargs):
        super(BaseState, cls).__init_subclass__()
        STATES[cls.get_name()] = cls

    def __init__(self, user):
        self.data = user.telegram_context
        self.user = user

    def create_state(self, state_name: str) ->'BaseState':
        return STATES[state_name](self.user)

    def get_intro_message(self):
        return self._intro_message

    def get_state(self) -> str:
        return self.data['state']

    def set_state(self, state_name: str):
        self.data['state'] = state_name

    async def get_back_state(self):
        return self.back

    async def consume(self, common_message):
        self.value = common_message.data

        if self.value == 'back':
            self.set_state(await self.get_back_state())

        elif self.value in self.ignorable_values:
            return []

        else:
            self.data[self.get_name()] = self.value
            self.text = common_message.text
            self.contact = common_message.contact
            await self.process()

        return await self.produce()

    async def process(self):
        """
        Updates user state and sets *is_unrecognized* value.
        """
        raise NotImplementedError()

    async def initialize(self, current_state) ->'BaseState':
        """
        Prepare context for the state.
        Base class returns itself but you can implement redirection logic.
        """
        return self

    async def produce(self) ->Sequence[BotMessage]:
        next_state = await self.create_state(self.get_state()).initialize(self.get_name())
        self.set_state(next_state.get_name())
        message = next_state.get_intro_message()
        if self.message_was_not_recognized:
            logger.warning('Unexpected user response on state %s: text=%s, value=%s',
                           self.get_name(), self.text, self.value)
            self.add_message('Unexpected response.')

        extra_messages = self.pop_messages()
        self.save_data()
        return message.to_sequence(extra_messages)

    def save_data(self):
        """
        Flag JSON fields as modified.
        """
        self.user.telegram_context = self.data
        flag_modified(self.user, 'telegram_context')
        flag_modified(self.user, 'external')

    def add_message(self, text):
        messages = self.data.get('messages', [])
        messages.append(text)
        self.data['messages'] = messages

    def pop_messages(self):
        messages = self.data.pop('messages', ())
        self.data['messages'] = ()
        return messages
