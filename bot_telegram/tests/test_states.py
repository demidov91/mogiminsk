import pytest
from bot_telegram.states import TimeState


class TestTimeState:
    @pytest.mark.parametrize('text,time', (
        ['1', '1:00'],
        ['2:12', '2:12'],
        ['115', '1:15'],
        ['1330', '13:30'],
    ))
    def test_consume__optimistic(self, text, time):
        tested = TimeState({}, None)
        tested.consume(text)
        assert tested.data['time'] == time
        assert tested.data['state'] == 'show'

    def test_consume__back(self):
        tested = TimeState({}, None)
        tested.consume('Back')
        assert tested.data['state'] == 'date'

    @pytest.mark.parametrize('text', (
        'back', '94', 'Hi!'
    ))
    def test_consume__not_correct(self, text):
        tested = TimeState({'state': 'time'}, None)
        tested.consume(text)
        assert tested.data['state'] == 'time'
        assert tested.message_was_not_recognized