"""
Mediator module for states.
"""
from bot_telegram.states import STATES, BaseState, WhereState
import logging

logger = logging.getLogger(__name__)


def get_state(update, request) -> BaseState:
    state_name = request['user'].telegram_context.get('state')

    if state_name in STATES:
        return STATES[request['user'].telegram_context['state']](update, request)

    raise ValueError(f'Unknown state {state_name}')


ERROR_MESSAGE = WhereState._intro_message.copy(
    text='Something went wrong...\n' + WhereState._intro_message.text
)
