"""
Mediator module for states.
"""
from bot_telegram.states import STATES, BaseState, WhereState
import logging

logger = logging.getLogger(__name__)


def get_state(value, user) -> BaseState:
    state_name = user.telegram_context.get('state')

    if state_name in STATES:
        return STATES[user.telegram_context['state']](value, user)

    raise ValueError(f'Unknown state {state_name}')


ERROR_MESSAGE = WhereState._intro_message.copy(
    text='Something went wrong...\n' + WhereState._intro_message.text
)
