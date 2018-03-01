import logging

from aiohttp_translation import gettext_lazy as _
from .base import BaseState
from bot.messages.base import BotMessage, BACK
from mogiminsk.services import ConversationService
from mogiminsk.settings import TG_CONTACT, VIBER_CONTACT
from bot_telegram.defines import TELEGRAM_BOT


logger = logging.getLogger(__name__)


class FeedbackState(BaseState):
    back = 'where'

    greeting_intro_message = BotMessage(
        _('Send me some feedback. '
            'What would you improve, '
            'what went wrong while using the bot?\n'
            'It will help me become better.'),
        buttons=[[BACK]],
        is_text_input=True
    )

    continue_intro_message = BotMessage(
        _('Add anything or press "Back" to return to booking trips.'),
        buttons=[[BACK]],
        is_text_input=True
    )

    def get_intro_message(self):
        if self.data.pop('feedback__continue', False):
            return self.continue_intro_message

        return self.greeting_intro_message

    async def process(self):
        bot = self.get_bot()

        logger.info(
            'Got %s feedback!\n---\n%s\n---\n'
            'User: first_name - %s; phone - %s\n'
            'Context: %s',
            bot, self.text, self.user.first_name, self.user.phone, self.data,
            extra={
                'tags': {
                    'event': 'feedback',
                    'bot': bot,
                },
            },
        )

        if not self.text:
            if bot == TELEGRAM_BOT:
                contact = TG_CONTACT

            else:
                contact = VIBER_CONTACT

            self.add_message(_(
                "Excuse me, I can't recognize your message :( "
                "Please, contact me directly at %s to tell what you wanted."
            ) % contact)

        else:
            ConversationService.add_user_message(
                self.user,
                self.text,
                self.data,
                bot
            )

        self.data['feedback__continue'] = True






