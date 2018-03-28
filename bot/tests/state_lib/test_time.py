import asyncio
from unittest.mock import patch

import pytest

from bot.state_lib.time import TimeState
# This import initializes state lib.
from bot.state_lib.time_period import TimePeriodState
from messager.input_data import InputMessage
from mogiminsk.factories import UserFactory


async def _stub_initialize(self, state_name):
    return self


class TestTimeState:
    @pytest.mark.parametrize('value,time,is_morning,is_evening', (
        ['first', '6:00', True, False],
        ['last', '21:30', False, True],
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

    @pytest.mark.parametrize('value', ('morning', 'day', 'evening'))
    def test_consume__navigation(self, value):
        tested = TimeState(UserFactory(), {'state': 'time', })
        tested.value = value
        asyncio.get_event_loop().run_until_complete(
            tested.process()
        )
        assert tested.data['state'] == 'time'
        assert tested.data['timeperiod'] == value

    @patch.object(TimePeriodState, 'initialize', _stub_initialize)
    def test_consume__back(self):
        tested = TimeState(UserFactory(), {})
        asyncio.get_event_loop().run_until_complete(
            tested.consume(InputMessage(data='back'))
        )
        assert tested.data['state'] == 'timeperiod'
