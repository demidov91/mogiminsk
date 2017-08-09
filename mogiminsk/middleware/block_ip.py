import logging

from aiohttp.web_exceptions import HTTPForbidden
from sqlalchemy.exc import IntegrityError

from ..utils import Session
from .block_ip_models import BlockedIp
from mogiminsk.settings import TELEGRAM_API_KEY


logger = logging.getLogger(__name__)


class KeyShield:
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

    async def middleware(self, app, handler):
        async def inner_handler(request):
            peername = request.transport.get_extra_info('peername')
            if peername is None:
                raise ValueError("Can't determine IP")

            host, port = peername
            if host in self.blocked_ip:
                logger.info(f'One more request from {host}')
                return HTTPForbidden()

            current_key = request.query.getone('key', None)
            if current_key != TELEGRAM_API_KEY:
                logger.warning(f'{host} will be blocked.')
                self.add_blocked_ip(host)
                return HTTPForbidden()

            return await handler(request)

        return inner_handler


