from mogiminsk.utils import threaded_session


class DbTest:
    def setup(self):
        self.session = threaded_session()

    def teardown(self):
        self.session.rollback()
        threaded_session.remove()