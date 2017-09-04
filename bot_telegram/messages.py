import datetime
from typing import List, Dict, Sequence, Collection
from mogiminsk.defines import DATE_FORMAT


class BotMessage:
    def __init__(self,
                 text: str='',
                 buttons: List[List[Dict]]=None,
                 text_buttons: List[List[str]]=None,
                 parse_mode: str = None):
        self.text = text
        self.parse_mode = parse_mode
        self.buttons = buttons
        self.text_buttons = text_buttons

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
        )
        return copy

    def to_sequence(self, prepend_messages: List[str]=()) -> Sequence['BotMessage']:
        messages = [BotMessage(x) for x in prepend_messages]
        messages.append(self)
        return messages


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
