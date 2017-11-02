import asyncio

import pytest

# This import initializes state lib.
from bot.state_lib.date import DateState
from bot.state_lib.time import TimeState
from messager.input_data import InputMessage
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

        tested = TimeState(UserFactory())
        tested.text = text
        asyncio.get_event_loop().run_until_complete(
            tested.process()
        )
        assert tested.data['time'] == expected
        assert tested.data['state'] == 'show'
        assert len(tested.data['trip_id_list']) == 1
        TimeState.get_trip_id_list.assert_called_once()

    def test_consume__back(self):
        tested = TimeState(UserFactory())
        asyncio.get_event_loop().run_until_complete(
            tested.consume(InputMessage(data='back'))
        )
        assert tested.data['state'] == 'date'

    @pytest.mark.parametrize('text', (
        'back', '94', 'Hi!'
    ))
    def test_consume__not_correct(self, text):
        tested = TimeState(UserFactory(telegram_context={'state': 'time'}))
        tested.text = text
        asyncio.get_event_loop().run_until_complete(
            tested.process()
        )
        assert tested.data['state'] == 'time'
        assert tested.message_was_not_recognized