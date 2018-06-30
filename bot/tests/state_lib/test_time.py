import asyncio
from unittest.mock import patch

import pytest

from bot.state_lib.time import TimeState
# This import initializes state lib.
from bot.state_lib.time_period import TimePeriodState
from messager.helper import Messager
from messager.input_data import InputMessage
from mogiminsk.factories import UserFactory


async def _stub_initialize(self, state_name):
    return self


class TestTimeState:
    @pytest.mark.parametrize('value,messager,is_morning,is_evening,expected', (
        ['first', Messager.VIBER, True, False, '6:30'],
        ['first', Messager.TELEGRAM, True, False, '6:00'],
        ['last', Messager.VIBER, False, True, '21:30'],
        ['last', Messager.TELEGRAM, False, True, '22:00'],
        ['7:40', None, False, False, '7:40'],
    ))
    @patch.object(TimeState, 'get_trip_id_list', return_value=[1])
    def test_consume__optimistic(self, patched, value, messager, is_morning, is_evening, expected):
        tested = TimeState(UserFactory(), {})
        tested.value = value
        tested.messager = messager
        asyncio.get_event_loop().run_until_complete(
            tested.process()
        )
        assert tested.data['state'] == 'show'
        assert tested.data['trip_id_list'] == [1]
        patched.assert_called_once_with(expected, is_morning, is_evening)

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
