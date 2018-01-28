import asyncio
from unittest.mock import patch

import pytest

# This import initializes state lib.
from bot.state_lib.time_period import TimePeriodState
from bot.state_lib.time import TimeState
from messager.input_data import InputMessage
from mogiminsk.factories import UserFactory


class TestTimeState:
    @pytest.mark.parametrize('value,time,is_morning,is_evening', (
        ['first', '5:59', True, False],
        ['last', '22:00', False, True],
        ['7:40', '7:40', False, False],
    ))
    @patch.object(TimeState, 'get_trip_id_list', return_value=[1])
    def test_consume__optimistic(self, patched, value, time, is_morning, is_evening):
        tested = TimeState(UserFactory(), {})
        tested.value = value
        asyncio.get_event_loop().run_until_complete(
            tested.process()
        )
        assert tested.data['state'] == 'show'
        assert tested.data['trip_id_list'] == [1]
        patched.assert_called_once_with(time, is_morning, is_evening)

    def test_consume__back(self):
        tested = TimeState(UserFactory(), {})
        asyncio.get_event_loop().run_until_complete(
            tested.consume(InputMessage(data='back'))
        )
        assert tested.data['state'] == 'timeperiod'
