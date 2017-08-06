from bot_telegram.states import STATES, BaseState, WhereState
import logging

logger = logging.getLogger(__name__)


def get_state(update, request) -> BaseState:
    return STATES[get_state_name(update.get_data(), request)](update, request)


def get_state_name(data, request) -> str:
    """
    Get state name either from data or from db.
    """
    if data and ('state' in data) and (data['state'] in STATES):
        return data['state']

    if request['user'] is not None and request['user'].telegram_state:
        return request['user'].telegram_state

    return 'initial'


ERROR_MESSAGE = WhereState._intro_message.copy(
    text='Something went wrong...\n' + WhereState._intro_message.text
)
