from bot_telegram.messages import BotMessage





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
