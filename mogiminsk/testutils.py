import asyncio
import os

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


def read_file(current_file: str, filename: str) ->bytes:
    """
    :param current_file: usually you have to provide __file__ var here.
    :param filename: path related to the :current_file:
    :return: Bytes of the file :filename: related to the :current_file:.
    """
    base_folder = os.path.dirname(current_file)
    with open(os.path.join(base_folder, filename), mode='rb') as f:
        return f.read()


class MockedAioHttpClient:
    def __init__(self, response):
        class Response:
            async def read(self):
                return response

            def release(self):
                pass

        self.response = Response()

    async def _request(self, *args, **kwargs):
        return self.response
