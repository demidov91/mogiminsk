from functools import lru_cache
import logging

from sqlalchemy import and_

from mogiminsk.models import Provider, ProviderContact
from mogiminsk.utils import Session, configure_session


logger = logging.getLogger(__name__)
db = None


@lru_cache(maxsize=10)
def get_provider(identifier):
    return db.query(Provider).filter(Provider.identifier == identifier).first()

def find_contact(provider, kind, value):
    return db.query(ProviderContact, Provider).filter(
        and_(
            Provider.identifier == provider,
            ProviderContact.kind == kind,
            ProviderContact.contact == value
        )
    ).first()

def build_contact(provider, kind, value) -> ProviderContact:
    provider_instance = get_provider(provider)
    if provider_instance is None:
        logger.warning('Provider %s is not found.', provider)
        return

    return ProviderContact(
        provider=provider_instance,
        kind=kind,
        contact=value
    )


def run():
    contacts = [
        {'provider': 'novaja_linija', 'kind': 'velcom', 'value': '+375293597597'},
        {'provider': 'novaja_linija', 'kind': 'mts', 'value': '+375293597597'},
        {'provider': 'novaja_linija', 'kind': 'web', 'value': 'https://7311.by'},

        {'provider': 'dve_stolicy', 'kind': 'velcom', 'value': '+375296024444'},
        {'provider': 'dve_stolicy', 'kind': 'mts', 'value': '+375336024444'},
        {'provider': 'dve_stolicy', 'kind': 'life', 'value': '+375256024444'},
        {'provider': 'dve_stolicy', 'kind': 'web', 'value': 'https://2stolict.com'},
    ]

    global db
    db = Session()

    try:
        for contact in contacts:
            if find_contact(**contact):
                continue

            model_to_save = build_contact(**contact)
            if model_to_save is None:
                continue

            db.add(model_to_save)
    except:
        logger.exception('Failed to load.')
        db.rollback()
    else:
        db.commit()


if __name__ == '__main__':
    run()