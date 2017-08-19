from bot_telegram.messages import BotMessage


def to_telegram_message(message: BotMessage):
    formatted = {
        'text': message.text,
    }

    if message.parse_mode:
        formatted['parse_mode'] = message.parse_mode

    if message.text_buttons:
        formatted['reply_markup'] = {
            'keyboard': TextButtonFormatter.format_list(message.text_buttons),
            'resize_keyboard': True,
            'one_time_keyboard': True,
        }

    elif message.buttons:
        formatted['reply_markup'] = {
            'inline_keyboard': InlineButtonFormatter.format_list(message.buttons),
        }

    return formatted


class ButtonFormatter:
    def __init__(self, button):
        self.button = button

    @classmethod
    def format_list(cls, buttons):
        return [
            [cls(x).format() for x in line] for line in buttons
        ]

    def format(self):
        raise NotImplementedError()


class InlineButtonFormatter(ButtonFormatter):
    def format(self):
        return {
            'text': self.button['text'],
            'callback_data': self.button['data'],
        }


class TextButtonFormatter(ButtonFormatter):
    def __init__(self, button):
        if isinstance(button, str):
            button = {
                'text': button,
                'type': 'text',
            }

        super().__init__(button)

    def format(self):
        data = {
            'text': self.button['text'],
        }
        if self.button['type'] == 'phone':
            data['request_contact'] = True

        return data
