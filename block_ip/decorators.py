from functools import wraps
import re
import logging

from aiohttp.web_exceptions import HTTPForbidden
from sqlalchemy.exc import IntegrityError

from block_ip.models import BlockedIp
from mogiminsk.utils import Session

logger = logging.getLogger(__name__)


class api_key(object):
    path_token_pattern = re.compile('/path-token:(?P<path_token>[\w-]+)/')

    def __init__(self, key: str):
        self.key = key
        self.blocked_ip = self.get_db_blocked_ip()

    def get_db_blocked_ip(self):
        db = Session()
        try:
            return {x[0] for x in db.query(BlockedIp.ip).all()}
        finally:
            db.close()

    def add_blocked_ip(self, ip: str):
        self.blocked_ip.add(ip)
        db = Session()
        try:
            db.add(BlockedIp(ip=ip))
            db.commit()
        except IntegrityError:
            logger.warning(f'{ip} blocked twice?')

        finally:
            db.close()

    def get_current_key(self, request):
        path_match = self.path_token_pattern.search(request.url.path)
        if path_match is None:
            return None

        return path_match.group('path_token')

    def __call__(self, func):
        @wraps(func)
        async def wrapper(cls, request):
            peername = request.transport.get_extra_info('peername')
            if peername is None:
                raise ValueError("Can't determine IP")

            host = None
            if peername:
                host, _ = peername

            if host in ('127.0.0.1', None) and \
                            request.headers.get('X-FORWARDED-FOR') not in ('127.0.0.1', None):
                host = request.headers['X-FORWARDED-FOR']

            logger.debug('Remote IP: %s', host)

            if host in self.blocked_ip:
                logger.info(f'One more request from {host}')
                return HTTPForbidden()

            current_key = self.get_current_key(request)
            if current_key != self.key:
                logger.warning(f'{host} will be blocked.')
                self.add_blocked_ip(host)
                return HTTPForbidden()

            return await func(cls, request)

        return wrapper




