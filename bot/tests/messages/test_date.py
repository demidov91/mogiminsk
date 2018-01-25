from freezegun import freeze_time

from bot.messages.date import OtherDateMessage


class TestOtherDateMessage:
    @freeze_time('2018-02-22')
    def test_get_tg_buttons__middle(self):
        tested = OtherDateMessage()
        buttons = tested.get_tg_buttons()

        assert len(buttons) == 3
        assert all(x['data'] == '-' for x in buttons[0][:3])
        assert buttons[0][3]['data'] == '22.02.2018'
        assert buttons[1][0]['data'] == '26.02.2018'
        assert buttons[1][6]['data'] == '04.03.2018'

    @freeze_time('2018-01-01')
    def test_get_tg_buttons__start(self):
        tested = OtherDateMessage()
        buttons = tested.get_tg_buttons()

        assert len(buttons) == 3
        assert buttons[0][0]['data'] == '01.01.2018'
        assert buttons[0][6]['data'] == '07.01.2018'
        assert buttons[1][0]['data'] == '08.01.2018'
        assert buttons[1][6]['data'] == '14.01.2018'

    @freeze_time('2018-01-07')
    def test_get_tg_buttons__end(self):
        tested = OtherDateMessage()
        buttons = tested.get_tg_buttons()

        assert len(buttons) == 3
        assert all(x['data'] == '-' for x in buttons[0][:6])
        assert buttons[0][6]['data'] == '07.01.2018'
        assert buttons[1][0]['data'] == '08.01.2018'
        assert buttons[1][6]['data'] == '14.01.2018'

    @freeze_time('2018-02-22')
    def test_get_viber_buttons__middle(self):
        tested = OtherDateMessage()
        buttons = tested.get_viber_buttons()

        assert len(buttons) == 11 + 1
        assert all(len(x) == 1 for x in buttons)
        assert buttons[0][0]['data'] == '22.02.2018'
        assert buttons[10][0]['data'] == '04.03.2018'

    @freeze_time('2018-01-01')
    def test_get_viber_buttons__start(self):
        tested = OtherDateMessage()
        buttons = tested.get_viber_buttons()

        assert len(buttons) == 14 + 1
        assert buttons[0][0]['data'] == '01.01.2018'
        assert buttons[13][0]['data'] == '14.01.2018'

    @freeze_time('2018-01-07')
    def test_get_viber_buttons__end(self):
        tested = OtherDateMessage()
        buttons = tested.get_viber_buttons()

        assert len(buttons) == 8 + 1
        assert buttons[0][0]['data'] == '07.01.2018'
        assert buttons[7][0]['data'] == '14.01.2018'