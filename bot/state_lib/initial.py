from bot.state_lib.base import BaseState


class InitialState(BaseState):

    async def process(self):
        self.set_state('where')

