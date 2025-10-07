import asyncio

from pytest import fixture


@fixture
def exception_handler():
    loop = asyncio.get_running_loop()
    old_exception_handler = loop.get_exception_handler()
    exceptions = []

    def exception_handler(*args, **kwargs):
        exceptions.append((args, kwargs))

    loop.set_exception_handler(exception_handler)

    try:
        yield
    finally:
        loop.set_exception_handler(old_exception_handler)
        assert not exceptions
