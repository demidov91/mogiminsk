import asyncio
from mogiminsk.utils import threaded_session, set_db


class DbTest:
    def setup(self):
        self.session = threaded_session()

    def teardown(self):
        self.session.rollback()
        threaded_session.remove()

    def run_async(self, method):
        async def local_session_initilizer():
            set_db(self.session)
            await method
            set_db(None)

        asyncio.get_event_loop().run_until_complete(local_session_initilizer())
