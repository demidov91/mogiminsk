from typing import List

from bot.messages.base import BotMessage


def build_basic_message(bot_message: BotMessage) -> dict:
    return {
        'text': bot_message.text,
        'type': 'text',
        'min_api_version': 4,
    }


def add_keyboard_into_message(viber_message: dict, bot_buttons: List[dict], hide_input: bool):
    buttons = tuple(format_button(x) for x in bot_buttons)

    viber_message['keyboard'] = {
        'Type': 'keyboard',
        'Buttons': buttons,
        'InputFieldState': 'hidden' if hide_input else 'regular',
    }


def format_button(bot_button: dict) ->dict:
    if bot_button.get('type') == 'phone':
        viber_button = {
            'ActionType': 'share-phone',
            'ActionBody': '---',
            'Text': bot_button['text'],
        }

    elif bot_button.get('type') == 'url':
        viber_button = {
            'ActionType': 'open-url',
            'ActionBody': bot_button['data'],
            'Text': bot_button['text'],
        }

    else:
        viber_button = {
            'ActionType': 'reply',
            'ActionBody': bot_button['data'],
            'Text': bot_button['text'],
        }

    viber_button.update(bot_button.get('viber', {}))
    return viber_button


def to_viber_message(bot_message: BotMessage, receiver) -> dict:
    viber_message = build_basic_message(bot_message)

    buttons = bot_message.get_viber_buttons()

    if buttons:
        add_keyboard_into_message(viber_message, buttons, hide_input=not bot_message.is_text_input)

    viber_message['receiver'] = receiver.id
    return viber_message