from tasklocal import local
import asyncio


class TestLocal:
    def test_nested(self):
        storage = local()

        async def f1():
            storage.some_data = 42
            assert storage.some_data == 42
            await f2()
            assert storage.some_data == 34

        async def f2():
            assert storage.some_data == 42
            storage.some_data = 34
            assert storage.some_data == 34

        asyncio.get_event_loop().run_until_complete(f1())

    def test_concurrent(self):
        storage = local()
        run_count = 0

        async def f1():
            nonlocal run_count
            run_count += 1
            assert not hasattr(storage, 'some_data')
            storage.some_data = 42
            assert hasattr(storage, 'some_data')
            await asyncio.sleep(0)
            assert storage.some_data == 42
            assert run_count == 2

        async def f2():
            nonlocal run_count
            run_count += 1
            assert not hasattr(storage, 'some_data')
            storage.some_data = 34
            await asyncio.sleep(0)
            assert storage.some_data == 34
            assert run_count == 2

        asyncio.get_event_loop().run_until_complete(asyncio.gather(f1(), f2()))

    def test_subsequent(self):
        storage = local()

        async def f1():
            storage.some_data = 42

        async def f2():
            assert storage.some_data == 42

        async def f_common():
            await f1()
            await f2()

        asyncio.get_event_loop().run_until_complete(f_common())

    def test_clear(self):
        storage = local()

        async def f():
            storage.field = 'value'
            assert hasattr(storage, 'field')
            storage.clear()
            assert not hasattr(storage, 'field')

        asyncio.get_event_loop().run_until_complete(f())
