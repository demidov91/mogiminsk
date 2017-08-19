from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import OtherDateBotMessage
from .date import DateState


class OtherDateState(DateState):
    @classmethod
    def get_intro_message(cls, data):
        return OtherDateBotMessage()

    def consume(self, text: str):
        super(OtherDateState, self).consume(text)
        self.data[DateState.get_name()] = self.data[self.get_name()]
