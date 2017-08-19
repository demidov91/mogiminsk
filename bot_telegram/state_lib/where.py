from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage


class WhereState(BaseState):
    """
    Store where we are going and ask WHEN?
    """
    _intro_message = BotMessage(
        text='Where are we going?',
        buttons=[[{
            'text': 'To Mogilev',
            'data': 'mogilev',
        }, {
            'text': 'To Minsk',
            'data': 'minsk',
        }]]
    )

    def get_intro_message(self):
        message = super().get_intro_message()

        if self.data.get('reset_reason'):
            message = message.copy()
            message.text = '{}\n{}'.format(self.data.pop('reset_reason'), message.text)

        return message

    def process(self):
        if self.value in ('mogilev', 'minsk'):
            self.set_state('date')

        else:
            self.message_was_not_recognized = True