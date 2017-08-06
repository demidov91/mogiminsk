import datetime
from typing import List, Dict
from urllib.parse import urlencode
from mogiminsk.defines import DATE_FORMAT


class BotMessage:
    # Text to show.
    text = None     # type: str

    # Array of arrays
    buttons = None  # type: List[List[Dict]]

    # Text which will be displayed in case of not parsed data on this step.
    _error_variant = None    # type: str

    def __init__(self, text, buttons=None, text_buttons: tuple=None, create_error_variant=True):
        self.text = text
        self.buttons = buttons
        self.text_buttons = text_buttons
        if create_error_variant:
            self._error_variant = BotMessage(
                'Unexpected response.\n' + self.text,
                self.buttons,
                create_error_variant=False
            )

    def error_variant(self):
        return self._error_variant

    def copy(self, text=None, buttons=None) ->'BotMessage':
        if text is None:
            text = self.text

        if buttons is None:
            buttons = self.buttons

        copy = BotMessage(text, buttons, create_error_variant=False)
        copy._error_variant = self._error_variant
        return copy

    def to_telegram_data(self, data):
        formatted = {
            'text': self.text,
        }

        if self.text_buttons:
            formatted['reply_markup'] = {
                'keyboard': self.text_buttons,
                'resize_keyboard': True,
                'one_time_keyboard': True,
            }

        elif self.buttons:
            formatted['reply_markup'] = {
                'inline_keyboard': [
                    [
                        self.to_telegram_inline_button(x, data) for x in line
                    ] for line in self.buttons
                ],
            }

        return formatted

    @classmethod
    def to_telegram_inline_button(cls, button, user_data):
        data = user_data.copy()
        data[data['state']] = button['data']
        return {
            'text': button['text'],
            'callback_data': urlencode(data),
        }


class DateBotMessage(BotMessage):
    def __init__(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        buttons = (
            (today.strftime('Today, %a'), today.strftime(DATE_FORMAT)),
            (tomorrow.strftime('Tomorrow, %a'), tomorrow.strftime(DATE_FORMAT)),
            ('Other', 'other'),
        )
        buttons = [
            [{'text': x[0], 'data': x[1]} for x in buttons],
            [{'text': 'Back', 'data': 'back',}],
        ]

        super(DateBotMessage, self).__init__('Choose the date', buttons)


class OtherDateBotMessage(BotMessage):
    def __init__(self):
        today = datetime.date.today()
        first_line = [today + datetime.timedelta(days=x) for x in range(7)]
        second_line = [today + datetime.timedelta(days=x) for x in range(7, 14)]

        buttons = [
            [{'text': str(x.day), 'data': x.strftime(DATE_FORMAT)} for x in first_line],
            [{'text': str(x.day), 'data': x.strftime(DATE_FORMAT)} for x in second_line],

            [{'text': 'Back', 'data': 'back', }],
        ]

        super(OtherDateBotMessage, self).__init__('Choose the date', buttons)

