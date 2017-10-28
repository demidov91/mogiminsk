from copy import deepcopy
from typing import List, Dict, Sequence

from aiohttp_translation import gettext_lazy as _


class BotMessage:
    def __init__(self,
                 text: str='',
                 buttons: List[List[Dict]]=None,
                 text_buttons: List[List[str]]=None,
                 parse_mode: str = None):
        self.text = self.build_text(text)
        self.parse_mode = parse_mode
        self.buttons = self.build_callback_buttons(buttons)
        self.text_buttons = self.build_text_buttons(text_buttons)

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

    def build_text_buttons(self, buttons: List[List[str]]) ->List[List[str]]:
        return buttons


# Standard 'Back' button.
BACK = {
    'text': _('Back'),
    'data': 'back',
}
