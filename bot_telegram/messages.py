import datetime
from typing import List, Dict
from urllib.parse import urlencode
from mogiminsk.defines import DATE_FORMAT


class BotMessage:
    # Message which will be displayed in case of not parsed data on this step.
    error_message = None    # type: BotMessage

    def __init__(self,
                 text: str,
                 buttons: List[List[Dict]]=None,
                 text_buttons: List[List[str]]=None,
                 parse_mode: str = None,
                 create_error_text=True):
        self.text = text
        self.parse_mode = parse_mode
        self.buttons = buttons
        self.text_buttons = text_buttons
        if create_error_text:
            self.error_message = BotMessage(
                'Unexpected response.\n' + self.text,
                self.buttons,
                create_error_text=False
            )

    def get_error_message(self):
        return self.error_message

    def copy(self, text=None, parse_mode=None, buttons=None) ->'BotMessage':
        if text is None:
            text = self.text

        if buttons is None:
            buttons = self.buttons

        if parse_mode is None:
            parse_mode = self.parse_mode

        copy = BotMessage(
            text=text,
            parse_mode=parse_mode,
            buttons=buttons,
            create_error_text=False
        )
        copy.error_message = self.error_message
        return copy

    def to_telegram_data(self):
        formatted = {
            'text': self.text,
        }

        if self.parse_mode:
            formatted['parse_mode'] = self.parse_mode

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
                        self.to_telegram_inline_button(x) for x in line
                    ] for line in self.buttons
                ],
            }

        return formatted

    @classmethod
    def to_telegram_inline_button(cls, button):
        return {
            'text': button['text'],
            'callback_data': button['data'],
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
