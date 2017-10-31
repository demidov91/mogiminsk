"""
Mediator module for states.
"""
import logging
from typing import Type

from bot.state_lib.base import STATES, BaseState
from bot import state_lib
from mogiminsk.utils import load_sub_modules

logger = logging.getLogger(__name__)


load_sub_modules(state_lib)


def get_state_class(state_name) -> Type[BaseState]:
    if state_name not in STATES:
        logger.warning('Unknown state: %s', state_name)
        state_name = 'initial'

    return STATES[state_name]