from bot_viber.utils.viber_messages import format_button


def test_format_button__text():
    button = {
        'text': 'hello',
        'data': 'world',
        'viber': {
            'Columns': 2,
            'Rows': 1,
        },
    }

    assert format_button(button) == {
        'ActionType': 'reply',
        'Text': 'hello',
        'ActionBody': 'world',
        'Columns': 2,
        'Rows': 1,
    }


def test_format_button__phone():
    button = {
        'text': 'hello',
        'type': 'phone',
        'viber': {
            'Columns': 1,
            'Rows': 1,
        },
    }

    assert format_button(button) == {
        'ActionType': 'share-phone',
        'Text': 'hello',
        'ActionBody': '---',
        'Columns': 1,
        'Rows': 1,
    }