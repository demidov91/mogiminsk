from typing import List

from bot.messages.base import BotMessage
from bot_viber.constants import VIBER_BUTTONS_WIDTH


def build_basic_message(bot_message: BotMessage) -> dict:
    return {
        'text': bot_message.text,
        'type': 'text',
        'min_api_version': 3,
    }


def add_keyboard_into_message(viber_message: dict, bot_buttons: List[List[dict]]):
    buttons = []

    for row in bot_buttons:
        viber_width = VIBER_BUTTONS_WIDTH // len(row)

        buttons.extend((
            format_button(x, viber_width) for x in row
        ))

    viber_message['keyboard'] = {
        'Type': 'keyboard',
        'Buttons': buttons,
    }


def format_button(bot_button: dict, width) ->dict:
    if bot_button.get('type') == 'phone':
        return {
            'Columns': width,
            'ActionType': 'share-phone',
            'ActionBody': '---',
            'Text': bot_button['text'],
        }

    return {
        'Columns': width,
        'ActionType': 'reply',
        'ActionBody': bot_button['data'],
        'Text': bot_button['text'],
    }


def to_viber_message(bot_message: BotMessage, receiver) -> dict:
    viber_message = build_basic_message(bot_message)

    if bot_message.buttons:
        add_keyboard_into_message(viber_message, bot_message.buttons)

    viber_message['receiver'] = receiver.id
    return viber_message