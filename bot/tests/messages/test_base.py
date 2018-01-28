from bot.messages.base import BotMessage


class TestBotMessage:
    def test_get_viber_buttons(self):
        tested = BotMessage(buttons=[[{
            'text': '1.1',
            'data': '1.1',
        }, {
            'text': '1.2',
            'data': '1.2',
        }, {
            'text': '1.3',
            'data': '1.3',
        }, ], [{
            'text': '2.1',
            'data': '2.1',
        }, {
            'text': '2.2',
            'data': '2.2',
        }, ], [{
            'text': '3.1',
            'data': '3.1',
        }, ],
        ])

        assert tested.get_viber_buttons() == [{
            'text': '1.1',
            'data': '1.1',
            'viber': {
                'Columns': 2,
            },
        }, {
            'text': '1.2',
            'data': '1.2',
            'viber': {
                'Columns': 2,
            },
        }, {
            'text': '1.3',
            'data': '1.3',
            'viber': {
                'Columns': 2,
            },
        }, {
            'text': '2.1',
            'data': '2.1',
            'viber': {
                'Columns': 3,
            },
        }, {
            'text': '2.2',
            'data': '2.2',
            'viber': {
                'Columns': 3,
            },
        }, {
            'text': '3.1',
            'data': '3.1',
            'viber': {
                'Columns': 6,
            },
        }, ]

    def test_get_viber_buttons__none(self):
        tested = BotMessage('Hello')
        assert tested.get_viber_buttons() is None
