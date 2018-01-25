import datetime
from itertools import chain

from babel.dates import format_date

from aiohttp_translation import gettext_lazy as _, get_active
from bot.messages.base import BotMessage, BACK
from mogiminsk.defines import DATE_FORMAT


class DateMessage(BotMessage):
    def __init__(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        buttons = (
            (
                _('Today, %s') % format_date(today, 'E', locale=get_active()),
                today.strftime(DATE_FORMAT)
            ),
            (
                _('Tomorrow, %s') % format_date(tomorrow, 'E', locale=get_active()),
                tomorrow.strftime(DATE_FORMAT)
            ),
            (
                _('Other'),
                'other'
            ),
        )
        buttons = [
            [{'text': x[0], 'data': x[1]} for x in buttons],
            [BACK],
        ]

        super(DateMessage, self).__init__(_('Choose the date'), buttons)


class OtherDateMessage(BotMessage):
    def _date_to_button(self, date: datetime.date):
        return {
            'data': date.strftime(DATE_FORMAT),
            '_date': date,
        }

    def _convert_buttons_to_tg(self):
        for line in self.buttons[:-1]:
            for button in line:
                button['text'] = str(button.pop('_date').day)

    def _convert_buttons_to_viber(self):
        for line in self.buttons[:-1]:
            for button in line:
                button['text'] = format_date(
                    button.pop('_date'),
                    'E, d MMMM',
                    locale=get_active()
                ).capitalize()

    def get_tg_buttons(self):
        self._convert_buttons_to_tg()
        missing_buttons = 7 - len(self.buttons[0])

        prepended = [{
            'text': b'\xE2\x9D\x8C'.decode('utf-8'),
            'data': '-',
        } for _ in range(missing_buttons)]

        self.buttons[0] = prepended + self.buttons[0]
        return self.buttons

    def get_viber_buttons(self):
        self._convert_buttons_to_viber()
        return [[x] for x in chain(*self.buttons)]

    def __init__(self):
        today = datetime.date.today()
        weekday = today.weekday()

        first_line = [
            self._date_to_button(today + datetime.timedelta(days=x))
            for x in range(7 - weekday)
        ]
        second_line = [
            self._date_to_button(today + datetime.timedelta(days=x))
            for x in range(7 - weekday, 14 - weekday)
        ]

        buttons = [
            first_line,
            second_line,
            [BACK],
        ]

        super(OtherDateMessage, self).__init__(_('Choose the date'),  buttons=buttons)
