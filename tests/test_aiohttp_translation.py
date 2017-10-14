import asyncio
import json

from aiohttp_translation import activate, LazyAwareJsonEncoder, gettext_lazy as _


class TestAiohttpTranslation:
    def test_gettext__ru(self):
        from aiohttp_translation import gettext as _

        async def inner():
            activate('ru')
            assert _('Test message') == 'Сие есть сущая тестовая строка'

        asyncio.get_event_loop().run_until_complete(inner())

    def test_gettext__be(self):
        from aiohttp_translation import gettext as _

        async def inner():
            activate('be')
            assert _('Test message') == 'Шмат тэстаў не бывае'

        asyncio.get_event_loop().run_until_complete(inner())

    def test_gettext_lazy(self):
        lazy_text = _('Test message')

        async def inner():
            activate('ru')
            assert str(lazy_text) == 'Сие есть сущая тестовая строка'

            activate('be')
            assert str(lazy_text) == 'Шмат тэстаў не бывае'

        asyncio.get_event_loop().run_until_complete(inner())


class TestLazyAwareJsonEncoder:
    def test_encode__lazy_text(self):
        from aiohttp_translation import gettext_lazy as _

        lazy_string = _('Test message')

        async def inner():
            activate('be')
            encoded = json.dumps(
                {'text': lazy_string},
                cls=LazyAwareJsonEncoder,
            )
            assert json.loads(encoded) == {
                'text': 'Шмат тэстаў не бывае',
            }

            activate('ru')
            encoded = json.dumps(
                {'text': lazy_string},
                cls=LazyAwareJsonEncoder,
            )
            assert json.loads(encoded) == {
                'text': 'Сие есть сущая тестовая строка',
            }

        asyncio.get_event_loop().run_until_complete(inner())
