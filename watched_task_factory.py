import asyncio

from loguru import logger

__all__ = ["install", "uninstall"]


class WatchedTaskFactory:
    def __init__(self):
        self.tasks = set()

    def done_callback(self, task: asyncio.Task):
        self.tasks.discard(task)

        try:
            task.result()
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.bind(task=task).exception("")

    def task_factory(self, loop, coro, **kwargs):
        task = asyncio.Task(coro, loop=loop, **kwargs)
        self.tasks.add(task)
        task.add_done_callback(self.done_callback)
        return task


_tf = WatchedTaskFactory()


def install():
    asyncio.get_running_loop().set_task_factory(_tf.task_factory)


def uninstall():
    asyncio.get_running_loop().set_task_factory(None)
