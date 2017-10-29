from bot.messages.date import OtherDateMessage
from .date import DateState


class OtherDateState(DateState):
    back = 'date'

    def get_intro_message(self):
        return OtherDateMessage()

    async def process(self):
        await super(OtherDateState, self).process()
        self.data[DateState.get_name()] = self.data[self.get_name()]
