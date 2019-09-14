from decimal import Decimal

import pytest

from mogiminsk.models import Provider, Trip


class TestProvider:
    @pytest.mark.parametrize('name,short_name', [
        ('2 столицы', '2 столицы'),
        ('Атлас/Новая Линия', 'Атлас'),
    ])
    def test_short_name(self, name, short_name):
        assert Provider(name=name).short_name == short_name


class TestTrip:
    @pytest.mark.parametrize('price,expected', [
        (9, False),
        (9.5, False),
        (10.0, True),
        (10, True),
        (Decimal('10.0'), True),
    ])
    def test_is_default_price(self, price, expected):
        assert Trip(cost=price).is_default_price() is expected
