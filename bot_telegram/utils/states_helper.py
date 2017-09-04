"""
Mediator module for states.
"""
import logging

from bot_telegram import state_lib
from bot_telegram.state_lib.base import STATES, BaseState
from bot_telegram.state_lib.where import WhereState
from mogiminsk.utils import load_sub_modules


logger = logging.getLogger(__name__)


load_sub_modules(state_lib)


def get_state(user) -> BaseState:
    state_name = user.telegram_context.get('state')

    if state_name in STATES:
        return STATES[user.telegram_context['state']](user)

    raise ValueError(f'Unknown state {state_name}')


def get_error_message():
    message = WhereState._intro_message
    return message.to_sequence(['Something went wrong...'])
