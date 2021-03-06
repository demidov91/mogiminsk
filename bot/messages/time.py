from aiohttp_translation import gettext_lazy as _
from .base import BotMessage, BACK


class AbstractPeriodMessage(BotMessage):
    viber_buttons = ()
    tg_buttons = ()

    def __init__(self):
        super().__init__(text=_('What time?'))

    def get_viber_buttons(self):
        return self.viber_buttons

    def get_tg_buttons(self):
        return self.tg_buttons


class MorningMessage(AbstractPeriodMessage):
    FIRST = 'first'

    viber_buttons = ({
        'text': _('Earlier \U0001f305'),
        'data': FIRST,
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '7:00',
        'data': '7:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '8:00',
        'data': '8:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '6:30',
        'data': '6:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '7:30',
        'data': '7:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '8:30',
        'data': '8:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '9:00',
        'data': '9:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '10:00',
        'data': '10:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '11:00',
        'data': '11:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '9:30',
        'data': '9:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '10:30',
        'data': '10:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': _('Later \U0001f31e'),
        'data': 'day',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    },
                     BACK
    )

    tg_buttons = (
        ({
            'text': _('Before 6:00'),
            'data': FIRST,
        }, {
            'text': '6:00',
            'data': '6:00',
        }, {
            'text': '7:00',
            'data': '7:00',
        },),
        ({
            'text': '8:00',
            'data': '8:00',
        }, {
            'text': '9:00',
            'data': '9:00',
        }, {
            'text': '10:00',
            'data': '10:00',
        }),
        (BACK, )
    )


class DayMessage(AbstractPeriodMessage):
    viber_buttons = ({
        'text': _('Earlier \U0001f305'),
        'data': 'morning',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '12:00',
        'data': '12:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '13:00',
        'data': '13:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '11:30',
        'data': '11:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '12:30',
        'data': '12:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '13:30',
        'data': '13:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '14:00',
        'data': '14:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '15:00',
        'data': '15:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '16:00',
        'data': '16:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '14:30',
        'data': '14:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '15:30',
        'data': '15:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': _('Later \U0001f307'),
        'data': 'evening',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    },
                     BACK
    )

    tg_buttons = (
        ({
            'text': '11:00',
            'data': '11:00',
        }, {
            'text': '12:00',
            'data': '12:00',
        }, {
            'text': '13:00',
            'data': '13:00',
        }, ),
        ({
            'text': '14:00',
            'data': '14:00',
        }, {
            'text': '15:00',
            'data': '15:00',
        }, {
            'text': '16:00',
            'data': '16:00',
        }),
        (BACK, )
    )


class EveningMessage(AbstractPeriodMessage):
    LAST = 'last'

    viber_buttons = ({
        'text': _('Earlier \U0001f31e'),
        'data': 'day',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '17:00',
        'data': '17:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '18:00',
        'data': '18:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '16:30',
        'data': '16:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '17:30',
        'data': '17:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '18:30',
        'data': '18:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '19:00',
        'data': '19:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '20:00',
        'data': '20:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '21:00',
        'data': '21:00',
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'bottom',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '19:30',
        'data': '19:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': '20:30',
        'data': '20:30',
        'viber': {
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    }, {
        'text': _('Later \U0001f307'),
        'data': LAST,
        'viber': {
            'TextSize': 'large',
            'TextVAlign': 'top',
            'Rows': 1,
            'Columns': 2,
        },
    },
                     BACK
    )

    tg_buttons = (({
            'text': '17:00',
            'data': '17:00',
        }, {
            'text': '18:00',
            'data': '18:00',
        }, {
            'text': '19:00',
            'data': '19:00',
        }, ),
                  ({
            'text': '20:00',
            'data': '20:00',
        }, {
            'text': '21:00',
            'data': '21:00',
        }, {
            'text': _('After 22:00'),
            'data': LAST,
        }, ),
                  (BACK, )
    )
