from collections import defaultdict
from copy import deepcopy
from typing import List, Dict, Sequence

from aiohttp_translation import gettext_lazy as _
from bot.constants import VIBER_BUTTONS_WIDTH


class BotMessage:
    def __init__(self,
                 text: str='',
                 buttons: List[List[Dict]]=None,
                 parse_mode: str = None,
                 is_tg_text_buttons=False,
                 is_text_input=False):
        self.text = self.build_text(text)
        self.buttons = self.build_callback_buttons(buttons)
        self.parse_mode = parse_mode
        self.is_tg_text_buttons = is_tg_text_buttons
        self.is_text_input=is_text_input

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
            buttons=deepcopy(buttons),
        )
        return copy

    def to_sequence(self, prepend_messages: List[str]=()) -> Sequence['BotMessage']:
        messages = [BotMessage(x) for x in prepend_messages]
        messages.append(self)
        return messages

    def build_text(self, text: str) ->str:
        return text

    def build_callback_buttons(self, buttons: List[List[dict]]) ->List[List[dict]]:
        return buttons

    def get_tg_buttons(self) ->List[List[dict]]:
        return self.buttons

    def get_viber_buttons(self) ->List[dict]:
        if not self.buttons:
            return None

        viber_buttons = []
        for row in self.buttons:
            viber_width = VIBER_BUTTONS_WIDTH // len(row)

            for button in row:
                button_with_width = defaultdict(dict, button)
                button_with_width['viber']['Columns'] = viber_width
                viber_buttons.append(button_with_width)

        return viber_buttons

    def __str__(self):
        return '{}: {}'.format(
            type(self),
            {
                'text': self.text,
                'buttons': self.buttons,
            }
        )

    def __repr__(self):
        return str(self)


# Standard 'Back' button.
BACK = {
    'text': _('Back'),
    'data': 'back',
}
