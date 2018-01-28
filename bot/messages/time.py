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
    FIRST_TIME = '6:00'

    viber_buttons = ({
        'text': _('Before %s') % FIRST_TIME,
        'data': FIRST,
        'viber': {
            'TextSize': 'large',
            'Rows': 2,
            'Columns': 2,
        },
    }, {
        'text': '6',
        'data': '6:00',
        'viber': {
            'TextSize': 'large',
            'Rows': 2,
            'Columns': 1,
        },
    }, {
        'text': '00',
        'data': '6:00',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'bottom',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '7',
        'data': '7:00',
        'viber': {
            'TextSize': 'large',
            'Rows': 2,
            'Columns': 1,
        },
    }, {
        'text': '00',
        'data': '7:00',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'bottom',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '30',
        'data': '6:30',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'top',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '30',
        'data': '7:30',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'top',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '8',
        'data': '8:00',
        'viber': {
            'TextSize': 'large',
            'Rows': 2,
            'Columns': 1,
        },
    }, {
        'text': '00',
        'data': '8:00',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'bottom',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '9',
        'data': '9:00',
        'viber': {
            'TextSize': 'large',
            'Rows': 2,
            'Columns': 1,
        },
    }, {
        'text': '00',
        'data': '9:00',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'bottom',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '10',
        'data': '10:00',
        'viber': {
            'TextSize': 'large',
            'Rows': 2,
            'Columns': 1,
        },
    }, {
        'text': '00',
        'data': '10:00',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'bottom',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '30',
        'data': '8:30',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'top',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '30',
        'data': '9:30',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'top',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    }, {
        'text': '30',
        'data': '10:30',
        'viber': {
            'TextSize': 'small',
            'TextVAlign': 'top',
            'TextHAlign': 'left',
            'Rows': 1,
            'Columns': 1,
        },
    },
                     BACK
    )

    tg_buttons = (
        ({
            'text': _('Before %s') % FIRST_TIME,
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
        'text': '11',
        'data': '11:00',
    }, {
        'text': '00',
        'data': '11:00',
    }, {
        'text': '30',
        'data': '11:30',
    }, {
        'text': '12',
        'data': '12:00',
    }, {
        'text': '00',
        'data': '12:00',
    }, {
        'text': '30',
        'data': '12:30',
    }, {
        'text': '13',
        'data': '13:00',
    }, {
        'text': '00',
        'data': '13:00',
    }, {
        'text': '30',
        'data': '13:30',
    }, {
        'text': '14',
        'data': '14:00',
    }, {
        'text': '00',
        'data': '14:00',
    }, {
        'text': '30',
        'data': '14:30',
    }, {
        'text': '15',
        'data': '10:00',
    }, {
        'text': '00',
        'data': '15:00',
    }, {
        'text': '30',
        'data': '15:30',
    }, {
        'text': '16',
        'data': '10:00',
    }, {
        'text': '00',
        'data': '16:00',
    }, {
        'text': '30',
        'data': '16:30',
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
            'data': '8:00',
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
    LAST_TIME = '22:00'

    viber_buttons = ({
        'text': '6',
        'data': '6:00',
    }, {
        'text': '00',
        'data': '6:00',
    }, {
        'text': '30',
        'data': '6:30',
    }, {
        'text': '17',
        'data': '17:00',
    }, {
        'text': '00',
        'data': '17:00',
    }, {
        'text': '30',
        'data': '17:30',
    }, {
        'text': '18',
        'data': '18:00',
    }, {
        'text': '00',
        'data': '18:00',
    }, {
        'text': '30',
        'data': '18:30',
    }, {
        'text': '19',
        'data': '19:00',
    }, {
        'text': '00',
        'data': '19:00',
    }, {
        'text': '30',
        'data': '19:30',
    }, {
        'text': '20',
        'data': '20:00',
    }, {
        'text': '00',
        'data': '20:00',
    }, {
        'text': '30',
        'data': '20:30',
    }, {
        'text': '21',
        'data': '21:00',
    }, {
        'text': '00',
        'data': '21:00',
    }, {
        'text': '30',
        'data': '21:30',
    }, {
        'text': _('After %s') % LAST_TIME,
        'data': LAST,
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
            'text': _('After %s') % LAST_TIME,
            'data': LAST,
        }, ),
                  (BACK, )
    )
