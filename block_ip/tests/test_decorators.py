import pytest

from unittest.mock import Mock
from block_ip.decorators import api_key


@pytest.mark.parametrize('path,expected', [
    ('/mogiminsk/viber/path-token:viber-simple-one/', 'viber-simple-one'),
    ('/mogiminsk/viber/', None),
])
def test_get_current_key(path, expected):
    request = Mock()
    request.url.path = path
    assert api_key('any').get_current_key(request) == expected