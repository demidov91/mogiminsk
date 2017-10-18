import asyncio

from mogiminsk.testutils import DbTest
from mogiminsk.factories import UserFactory
from mogiminsk.services import ConversationService


class TestConversationService(DbTest):
    def test_add_user_message(self):
        async def f():
            user = UserFactory()
            assert ConversationService.filter_by(user=user).count() == 0
            ConversationService.add_user_message(user, 'Hello world!')
            assert ConversationService.filter_by(user=user).count() == 1
            message = ConversationService.filter_by(user=user).first()
            assert message.is_user_message

        self.run_async(f())

    def test_add_bot_message(self):
        async def f():
            user = UserFactory()
            ConversationService.add_bot_message(user, 'Hello world!')
            assert ConversationService.filter_by(user=user).count() == 1
            message = ConversationService.filter_by(user=user).first()
            assert message.is_user_message is False

        self.run_async(f())
