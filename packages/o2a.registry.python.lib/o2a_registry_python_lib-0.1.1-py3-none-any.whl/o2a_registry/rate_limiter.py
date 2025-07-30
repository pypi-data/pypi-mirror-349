import asyncio
from asyncio import Task, Future
from datetime import datetime
from typing import Tuple, Optional, Coroutine, Any, TypeVar

T = TypeVar("T")


class RateLimiter:
    def __init__(self, req_per_sec: int):
        self._queue = asyncio.Queue[Tuple[Coroutine, Future]]()
        self._req_per_sec = req_per_sec
        self._runner: Optional[Task] = None

    async def __call__(self, request: Coroutine[Any, Any, T]) -> T:
        await self._start_runner()
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        await self._queue.put((request, future))
        return await future

    async def _start_runner(self):
        if self._runner is None:
            loop = asyncio.get_running_loop()
            self._runner = loop.create_task(self._run())

    async def _run(self) -> None:
        while True:
            request, future = await self._queue.get()
            before = datetime.now()
            await self._execute(request, future)
            after = datetime.now()

            time_taken = (after - before).total_seconds()
            sleep_time = max(0.0, 1 / self._req_per_sec - time_taken)
            await asyncio.sleep(sleep_time)

    @staticmethod
    async def _execute(request: Coroutine, fut: Future) -> None:
        try:
            result = await request
            fut.set_result(result)
        except Exception as e:
            fut.set_exception(e)

    async def stop_runner(self):
        self._runner.cancel()
