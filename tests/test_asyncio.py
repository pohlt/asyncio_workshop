import asyncio
from contextlib import contextmanager

from pytest import mark


async def func_ok(v: int):
    await asyncio.sleep(1)
    return 42 * v


async def func_fail(v: int):
    await asyncio.sleep(1)
    raise ZeroDivisionError


@mark.asyncio
async def test_asyncio_ok():
    await func_ok(5)


@mark.asyncio
async def test_asyncio_fail():
    await func_fail(5)


# see https://github.com/pytest-dev/pytest-asyncio/issues/205
@mark.asyncio
async def test_asyncio_fail_unnoticed():
    asyncio.create_task(func_fail(5))
    await asyncio.sleep(2)


@contextmanager
def exception_handler():
    loop = asyncio.get_running_loop()
    old_exception_handler = loop.get_exception_handler()
    exceptions = []
    loop.set_exception_handler(lambda loop, context: exceptions.append(context["exception"]))

    try:
        yield
    finally:
        loop.set_exception_handler(old_exception_handler)
        if exceptions:
            raise ExceptionGroup("exception(s) in loop", exceptions)


@mark.asyncio
async def test_asyncio_fail_noticed():
    with exception_handler():
        for _ in range(1):
            asyncio.create_task(func_fail(5))
        await asyncio.sleep(2)
