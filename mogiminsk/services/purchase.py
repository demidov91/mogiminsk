from .base import BaseService
from mogiminsk.models import Purchase


class PurchaseService(BaseService):
    model = Purchase
