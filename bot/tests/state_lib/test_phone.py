import pytest


from mogiminsk.factories import UserFactory
from bot.state_lib.phone import PhoneState
from messager.input_data import InputContact


class TestPhone:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('is_user_phone', [True, False])
    async def test_process__by_contact(self, is_user_phone):
        user = UserFactory()
        tested = PhoneState(user, {})
        tested.contact = InputContact(phone='375292020327', is_user_phone=is_user_phone)
        await tested.process()
        assert user.phone == '375292020327'

    @pytest.mark.asyncio
    @pytest.mark.parametrize('text', [
        '375292020327',
        '+375292020327',
        'My phone: 375292020327',
        ' 375292020327  ',
        'Так, 375292020327 ',
        '375 29 2020327',
        '+375 (29) 2020327',
        '202 and +375 (29) 2020327',
        '292020327',
    ])
    async def test_process__valid_text(self, text):
        user = UserFactory()
        tested = PhoneState(user, {})
        tested.text = text
        await tested.process()
        assert user.phone == '375292020327'

    @pytest.mark.asyncio
    @pytest.mark.parametrize('text', [
        '75292020327',
        '29 and 2020327',
        'A3N7Y5t2e9x2t0w2i0t3h2i7n',
    ])
    async def test_process__invalid_text(self, text):
        user = UserFactory()
        tested = PhoneState(user, {})
        tested.text = text
        await tested.process()
        assert tested.message_was_not_recognized


