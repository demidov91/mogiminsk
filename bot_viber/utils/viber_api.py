from viberbot.api.viber_requests import ViberRequest, ViberMessageRequest
from viberbot.api.messages import TextMessage
from viberbot.api.user_profile import UserProfile

from messager.input_data import InputMessage
from mogiminsk.models import User
from mogiminsk.services import UserService


def get_input_message(update: ViberRequest) ->InputMessage:
    if isinstance(update, ViberMessageRequest):
        if isinstance(update.message, TextMessage):
            return InputMessage(text=update.message.text)

    return None


def get_viber_user(update: ViberRequest) ->str:
    if isinstance(update, ViberMessageRequest):
        return update.sender

    return None


def get_db_user(remote_user: UserProfile) -> User:
    return UserService.filter_by(viber_id=remote_user.id).first()


def get_or_create_user(remote_user: UserProfile):
    user = get_db_user(remote_user)
    if user is None:
        user = UserService.add(
            viber_context={'state': 'initial'},
            viber_id=remote_user.id
        )

    return user