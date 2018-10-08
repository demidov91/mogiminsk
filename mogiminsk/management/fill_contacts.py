from functools import lru_cache
import logging

from sqlalchemy import and_

from mogiminsk.models import Provider, ProviderContact
from mogiminsk.utils import threaded_session


logger = logging.getLogger(__name__)


@lru_cache(maxsize=10)
def get_provider(identifier):
    return threaded_session().query(Provider).filter(Provider.identifier == identifier).first()


def find_contact(provider, kind, value):
    return threaded_session.query(ProviderContact, Provider).filter(
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
        {'provider': 'novaja_linija', 'kind': 'mts', 'value': '+375333597597'},
        {'provider': 'novaja_linija', 'kind': 'web', 'value': 'https://7311.by'},

        {'provider': 'dve_stolicy', 'kind': 'velcom', 'value': '+375296024444'},
        {'provider': 'dve_stolicy', 'kind': 'mts', 'value': '+375336024444'},
        {'provider': 'dve_stolicy', 'kind': 'life', 'value': '+375256024444'},
        {'provider': 'dve_stolicy', 'kind': 'web', 'value': 'https://2stolict.com'},

        {'provider': 'grand_express', 'kind': 'velcom', 'value': '+375291602222'},
        {'provider': 'grand_express', 'kind': 'velcom', 'value': '+375291612222'},
        {'provider': 'grand_express', 'kind': 'mts', 'value': '+375295462222'},
        {'provider': 'grand_express', 'kind': 'mts', 'value': '+375295452222'},
        {'provider': 'grand_express', 'kind': 'life', 'value': '+375255102222'},
        {'provider': 'grand_express', 'kind': 'web', 'value': 'http://grandexpress.by'},

        {'provider': 'stolica_plus', 'kind': 'velcom', 'value': '+375293522215'},
        {'provider': 'stolica_plus', 'kind': 'mts', 'value': '+375333522215'},
        {'provider': 'stolica_plus', 'kind': 'life', 'value': '+375259560707'},
        {'provider': 'stolica_plus', 'kind': 'web', 'value': 'https://m4minsk.by'},

        {'provider': 'minsk_express', 'kind': 'velcom', 'value': '+375447885533'},
        {'provider': 'minsk_express', 'kind': 'mts', 'value': '+375297885533'},
        {'provider': 'minsk_express', 'kind': 'life', 'value': '+375257885533'},
        {'provider': 'minsk_express', 'kind': 'velcom', 'value': '+375447886633'},
        {'provider': 'minsk_express', 'kind': 'mts', 'value': '+375297886633'},
        {'provider': 'minsk_express', 'kind': 'life', 'value': '+375257886633'},
        {'provider': 'minsk_express', 'kind': 'web', 'value': 'http://mogilevminsk.by'},

        {'provider': 'avtoslava', 'kind': 'velcom', 'value': '+375445555161'},
        {'provider': 'avtoslava', 'kind': 'mts', 'value': '+375295555161'},
        {'provider': 'avtoslava', 'kind': 'life', 'value': '+375256842235'},
        {'provider': 'avtoslava', 'kind': 'web', 'value': 'http://avto-slava.by'},
    ]

    db = threaded_session()

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