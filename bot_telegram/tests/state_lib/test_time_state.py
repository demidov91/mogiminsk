import pytest

from bot_telegram.state_lib.time import TimeState
from mogiminsk.factories import UserFactory


class TestTimeState:
    @pytest.mark.parametrize('text,expected', (
        ['1', '1:00'],
        ['2:12', '2:12'],
        ['115', '1:15'],
        ['1330', '13:30'],
    ))
    def test_consume__optimistic(self, text, expected, mocker):
        mocker.patch.object(TimeState, 'get_trip_id_list')
        TimeState.get_trip_id_list.return_value = [1]

        tested = TimeState(None, UserFactory())
        tested.consume(text)
        assert tested.data['time'] == expected
        assert tested.data['state'] == 'show'
        assert len(tested.data['trip_id_list']) == 1
        TimeState.get_trip_id_list.assert_called_once()

    def test_consume__back(self):
        tested = TimeState('back', UserFactory())
        tested.consume('Back')
        assert tested.data['state'] == 'date'

    @pytest.mark.parametrize('text', (
        'back', '94', 'Hi!'
    ))
    def test_consume__not_correct(self, text):
        tested = TimeState(None, UserFactory(telegram_context={'state': 'time'}))
        tested.consume(text)
        assert tested.data['state'] == 'time'
        assert tested.message_was_not_recognized