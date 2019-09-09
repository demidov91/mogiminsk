import pytest

from mogiminsk.models import Provider


class TestTrip:
    @pytest.mark.parametrize('name,short_name', [
        ('2 столицы', '2 столицы'),
        ('Атлас/Новая Линия', 'Атлас'),
    ])
    def test_short_name(self, name, short_name):
        assert Provider(name=name).short_name == short_name
