import logging

from aiohttp_translation import gettext_lazy as _
from .base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.services import ConversationService
from mogiminsk.models import Conversation


logger = logging.getLogger(__name__)


class FeedbackState(BaseState):
    back = 'where'

    greeting_intro_message = BotMessage(
        _('Send me some feedback. '
            'What would you improve, '
            'what went wrong while using the bot?\n'
            'It will help me become better.'), buttons=[[{
                'text': _('Back'),
                'data': 'back',
    }]])

    continue_intro_message = BotMessage(
        _('Add anything or press "Back" to return to booking trips.'),
        buttons=[[{
            'text': _('Back'),
            'data': 'back',
        }]]
    )

    def get_intro_message(self):
        if self.data.pop('feedback__continue', False):
            return self.continue_intro_message

        return self.greeting_intro_message

    async def process(self):
        logger.info(
            'Got feedback! %s\n'
            'User: first_name - %s; phone - %s\n'
            'Context: %s',
            self.text, self.user.first_name, self.user.phone, self.data
        )

        if not self.text:
            self.add_message(_(
                "Excuse me, I can't recognize your message :( "
                "Please, contact me directly at %s to tell what you wanted."
            ) % '@dzimdziam')

        else:
            ConversationService.add_user_message(
                self.user,
                self.text, Conversation.MESSENGER_TELEGRAM
            )

        self.data['feedback__continue'] = True






