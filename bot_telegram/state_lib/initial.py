from bot_telegram.state_lib.base import BaseState


class InitialState(BaseState):
    is_callback_state = False

    def process(self):
        self.set_state('where')

