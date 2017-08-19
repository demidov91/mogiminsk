from bot_telegram.utils.messages_helper import (
    TextButtonFormatter,
    InlineButtonFormatter
)


class TestTextButtonFormatter:
    def test_format_list(self):
        source = ['Ivan', {
            'type': 'phone',
            'text': 'hello',
        }]
        assert TextButtonFormatter.format_list([source]) == [
            [
                {'text': 'Ivan', },
                {'text': 'hello', 'request_contact': True, },
            ]
        ]
        

class TestInlineButtonFormatter:
    def test_format(self):
        source = {
            'text': 'Hello',
            'data': 'world',
        }
        assert InlineButtonFormatter(source).format() == {
            'text': 'Hello',
            'callback_data': 'world',
        }
