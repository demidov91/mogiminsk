from bot_telegram.messages import OtherDateBotMessage
from .date import DateState


class OtherDateState(DateState):
    back = 'date'

    def get_intro_message(self):
        return OtherDateBotMessage()

    async def process(self):
        await super(OtherDateState, self).process()
        self.data[DateState.get_name()] = self.data[self.get_name()]
