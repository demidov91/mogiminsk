import asyncio

from mogiminsk.factories import UserFactory
from mogiminsk.testutils import DbTest
from mogiminsk.utils import get_db
from bot.state_lib.phone import PhoneState
from messager.input_data import InputContact


class TestPhone(DbTest):
    def test_process__new_user(self):
        user = UserFactory()
        tested = PhoneState(user, {})
        tested.contact = InputContact(phone='375292020327', is_user_phone=True)
        self.run_async(tested.process())
        assert user.phone == '375292020327'

    def test_process__fake_user(self):
        user = UserFactory()
        tested = PhoneState(user, {})
        tested.contact = InputContact(phone='375292020327', is_user_phone=False)
        self.run_async(tested.process())
        assert user.phone is None
        assert tested.message_was_not_recognized

    def test_process__viber_into_tg(self):
        tg_user = UserFactory(
            phone='375292020327',
            telegram_id=12345,
            telegram_context={'any': 'data'},
        )

        viber_user = UserFactory(
            viber_id='another-user',
            viber_context={'other': 'data'}
        )

        tested = PhoneState(viber_user, {})
        tested.contact = InputContact(phone='375292020327', is_user_phone=True)
        self.run_async(tested.process())

        assert tested.user == tg_user
        assert tested.user.telegram_id == 12345
        assert tested.user.viber_id == 'another-user'
        assert tested.user.telegram_context == {'any': 'data'}
        assert tested.user.viber_context == {'other': 'data'}

    def test_process__tg_into_viber(self):
        tg_user = UserFactory(
            telegram_id=12345,
            telegram_context={'any': 'data'}
        )

        viber_user = UserFactory(
            phone='375292020327',
            viber_id='another-user',
            viber_context={'other': 'data'}
        )

        tested = PhoneState(tg_user, {})
        tested.contact = InputContact(phone='375292020327', is_user_phone=True)
        self.run_async(tested.process())

        assert tested.user == viber_user
        assert tested.user.telegram_id == 12345
        assert tested.user.viber_id == 'another-user'
        assert tested.user.telegram_context == {'any': 'data'}
        assert tested.user.viber_context == {'other': 'data'}
