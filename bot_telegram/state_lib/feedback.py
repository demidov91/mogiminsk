from aiohttp_translation import gettext_lazy as _
from .base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.services import ConversationService


class FeedbackState(BaseState):
    back = 'where'

    greeting_intro_message = BotMessage(
        _('Send me some feedback, '
            'what would you improve, '
            'what went wrong while using the bot. '
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
        if not self.text:
            self.add_message(_(
                "Excuse me, I can't recognize your message :( "
                "Please, contact me directly at %s to tell what you wanted."
            ) % '@dzimdziam')

        else:
            ConversationService.add_user_message(self.user, self.text)

        self.data['feedback__continue'] = True






