import asyncio

from aiohttp_translation import activate, gettext as _


class TestAiohttpTranslation:
    def test_gettext__ru(self):
        async def inner():
            activate('ru')
            assert _('Test message') == 'Сие есть сущая тестовая строка'

        asyncio.get_event_loop().run_until_complete(inner())

    def test_gettext__be(self):
        async def inner():
            activate('be')
            assert _('Test message') == 'Шмат тэстаў не бывае'

        asyncio.get_event_loop().run_until_complete(inner())