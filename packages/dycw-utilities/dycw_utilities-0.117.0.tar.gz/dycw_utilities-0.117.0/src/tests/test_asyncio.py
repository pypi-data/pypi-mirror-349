from __future__ import annotations

from asyncio import (
    CancelledError,
    Event,
    PriorityQueue,
    Queue,
    TaskGroup,
    run,
    sleep,
    timeout,
)
from collections import Counter
from dataclasses import dataclass, field
from functools import partial
from itertools import chain, count
from re import search
from typing import TYPE_CHECKING, Self, override

from hypothesis import Phase, given, settings
from hypothesis.strategies import (
    DataObject,
    data,
    integers,
    just,
    lists,
    none,
    permutations,
    sampled_from,
)
from pytest import approx, mark, param, raises

from utilities.asyncio import (
    AsyncLoopingService,
    AsyncService,
    EnhancedTaskGroup,
    ExceptionProcessor,
    InfiniteLooper,
    InfiniteLooperError,
    InfiniteQueueLooper,
    InfiniteQueueLooperError,
    QueueProcessor,
    UniquePriorityQueue,
    UniqueQueue,
    get_event,
    get_items,
    get_items_nowait,
    put_items,
    put_items_nowait,
    sleep_dur,
    sleep_until,
    sleep_until_rounded,
    stream_command,
    timeout_dur,
)
from utilities.dataclasses import replace_non_sentinel
from utilities.datetime import MILLISECOND, datetime_duration_to_timedelta, get_now
from utilities.hypothesis import sentinels, text_ascii
from utilities.iterables import one, unique_everseen
from utilities.pytest import skipif_windows
from utilities.sentinel import Sentinel, sentinel
from utilities.timer import Timer

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from utilities.types import Coroutine1, Duration, MaybeCallableEvent, MaybeType


class TestAsyncLoopingService:
    async def test_main(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncLoopingService):
            counter: int = 0

            @override
            async def _run(self) -> None:
                self.counter += 1

        async with Example(duration=1.0, sleep=0.1) as service:
            pass
        assert 5 <= service.counter <= 15

    async def test_cancel(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncLoopingService):
            counter: int = 0

            @override
            async def _run(self) -> None:
                self.counter += 1
                if self.counter >= 10:
                    raise CancelledError

        async with Example(sleep=0.1) as service:
            pass
        assert 5 <= service.counter <= 15

    async def test_sleep_after_failure(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncLoopingService):
            counter: int = 0
            errors: Counter[type[Exception]] = field(default_factory=Counter)

            @override
            async def _run(self) -> None:
                self.counter += 1
                if self.counter % 2 == 0:
                    raise ValueError

            @override
            async def _run_failure(self, error: Exception, /) -> None:
                self.errors.update([type(error)])

        async with Example(duration=1.0, sleep=0.1) as service:
            pass
        assert 5 <= service.counter <= 15
        assert 3 <= service.errors[ValueError] <= 7

    async def test_failure(self) -> None:
        class CustomError(Exception): ...

        @dataclass(kw_only=True)
        class Example(AsyncLoopingService):
            counter: int = 0
            failed: bool = False

            @override
            async def _run(self) -> None:
                self.counter += 1
                if self.counter >= 5:
                    raise CustomError

        with raises(CustomError):
            async with Example(sleep=0.1):
                pass


class TestAsyncService:
    async def test_main(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start(self) -> None:
                self.running = True

            @override
            async def stop(self) -> None:
                self.running = False
                await super().stop()

        service = Example(duration=0.1)
        for _ in range(2):
            assert not service.running
            async with service:
                assert service.running
                async with service:
                    assert service.running
                assert service.running
            assert not service.running

    async def test_timeout(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start(self) -> None:
                self.running = True

            @override
            async def stop(self) -> None:
                self.running = False
                await super().stop()

        service = Example()
        try:
            async with timeout_dur(duration=0.05), service:
                await sleep(0.1)
        except TimeoutError:
            assert not service.running

    @mark.parametrize(
        ("duration", "expected"),
        [
            param(0.5, approx(5, abs=1)),
            param(1.0, approx(10, abs=1)),
            param(1.5, 10),
            param(None, 10),
        ],
    )
    async def test_cancellation(
        self, *, duration: Duration | None, expected: int
    ) -> None:
        class Example(AsyncService):
            counter: int = 0

            @override
            async def _start(self) -> None:
                for _ in range(10):
                    self.counter += 1
                    await sleep(0.1)
                raise CancelledError

        async with Example(duration=duration) as service:
            ...
        assert service.counter == expected

    async def test_extra_context_managers(self) -> None:
        @dataclass(kw_only=True)
        class Inner(AsyncService):
            duration: Duration | None = 0.1
            running: bool = False

            @override
            async def _start(self) -> None:
                self.running = True

            @override
            async def stop(self) -> None:
                self.running = False
                await super().stop()

        @dataclass(kw_only=True)
        class Outer(AsyncService):
            duration: Duration | None = 0.1
            running: bool = False
            inner: Inner = field(default_factory=Inner, init=False, repr=False)

            @override
            async def _start(self) -> None:
                self.running = True
                _ = await self._stack.enter_async_context(self.inner)

            @override
            async def stop(self) -> None:
                self.running = False
                await super().stop()

        outer = Outer()
        for _ in range(2):
            assert not outer.running
            assert not outer.inner.running
            async with outer:
                assert outer.running
                assert outer.inner.running
            assert not outer.running
            assert not outer.inner.running

    def test_repr(self) -> None:
        class Example(AsyncService):
            @override
            async def _start(self) -> None:
                await sleep(0.01)

        service = Example()
        result = repr(service)
        expected = "TestAsyncService.test_repr.<locals>.Example(duration=None)"
        assert result == expected


class TestEnhancedTaskGroup:
    async def test_max_tasks_disabled(self) -> None:
        with Timer() as timer:
            async with EnhancedTaskGroup() as tg:
                for _ in range(10):
                    _ = tg.create_task(sleep(0.01))
        assert timer <= 0.05

    async def test_max_tasks_enabled(self) -> None:
        with Timer() as timer:
            async with EnhancedTaskGroup(max_tasks=2) as tg:
                for _ in range(10):
                    _ = tg.create_task(sleep(0.01))
        assert timer >= 0.05

    async def test_timeout_pass(self) -> None:
        async with EnhancedTaskGroup(timeout=0.2) as tg:
            _ = tg.create_task(sleep(0.1))

    async def test_timeout_fail(self) -> None:
        with raises(ExceptionGroup) as exc_info:
            async with EnhancedTaskGroup(timeout=0.05) as tg:
                _ = tg.create_task(sleep(0.1))
        assert len(exc_info.value.exceptions) == 1
        error = one(exc_info.value.exceptions)
        assert isinstance(error, TimeoutError)

    async def test_custom_error(self) -> None:
        class CustomError(Exception): ...

        with raises(ExceptionGroup) as exc_info:
            async with EnhancedTaskGroup(timeout=0.05, error=CustomError) as tg:
                _ = tg.create_task(sleep(0.1))
        assert len(exc_info.value.exceptions) == 1
        error = one(exc_info.value.exceptions)
        assert isinstance(error, CustomError)


class TestExceptionProcessor:
    async def test_main(self) -> None:
        processor = ExceptionProcessor()

        class CustomError(Exception): ...

        with raises(CustomError):  # noqa: PT012
            async with processor:
                processor.enqueue(CustomError)
                await sleep(0.1)


class TestGetEvent:
    def test_event(self) -> None:
        event = Event()
        assert get_event(event=event) is event

    @given(event=none() | sentinels())
    def test_none_or_sentinel(self, *, event: None | Sentinel) -> None:
        assert get_event(event=event) is event

    def test_replace_non_sentinel(self) -> None:
        @dataclass(kw_only=True, slots=True)
        class Example:
            event: Event = field(default_factory=Event)

            def replace(
                self, *, event: MaybeCallableEvent | Sentinel = sentinel
            ) -> Self:
                return replace_non_sentinel(self, event=get_event(event=event))

        event1, event2, event3 = Event(), Event(), Event()
        obj = Example(event=event1)
        assert obj.event is event1
        assert obj.replace().event is event1
        assert obj.replace(event=event2).event is event2
        assert obj.replace(event=lambda: event3).event is event3

    def test_callable(self) -> None:
        event = Event()
        assert get_event(event=lambda: event) is event


class TestInfiniteLooper:
    @given(n=integers(10, 11))
    async def test_main(self, *, n: int) -> None:
        class TrueError(BaseException): ...

        class FalseError(BaseException): ...

        @dataclass(kw_only=True)
        class Example(InfiniteLooper[bool]):
            counter: int = 0

            @override
            async def _initialize(self) -> None:
                self.counter = 0

            @override
            async def _core(self) -> None:
                self.counter += 1
                if self.counter >= n:
                    self._set_event(n % 2 == 0)

            @override
            def _yield_events_and_exceptions(
                self,
            ) -> Iterator[tuple[bool, MaybeType[BaseException]]]:
                yield (True, TrueError)
                yield (False, FalseError)

        looper = Example(sleep_core=0.1)
        match n % 2 == 0:
            case True:
                with raises(TrueError):
                    _ = await looper()
            case False:
                with raises(FalseError):
                    _ = await looper()

    async def test_hashable(self) -> None:
        class CustomError(Exception): ...

        @dataclass(kw_only=True, unsafe_hash=True)
        class Example(InfiniteLooper[None]):
            @override
            def _yield_events_and_exceptions(
                self,
            ) -> Iterator[tuple[None, MaybeType[Exception]]]:
                yield (None, CustomError)

        looper = Example(sleep_core=0.1)
        _ = hash(looper)

    async def test_with_coroutine_self_set_event(self) -> None:
        external: int = 0

        async def inc_external(obj: Example, /) -> None:
            nonlocal external
            while True:
                external += 1
                obj.counter += 1
                await sleep(0.05)

        class CustomError(Exception): ...

        @dataclass(kw_only=True)
        class Example(InfiniteLooper[None]):
            initializations: int = 0
            counter: int = 0

            @override
            async def _initialize(self) -> None:
                self.initializations += 1
                self.counter = 0

            @override
            async def _core(self) -> None:
                self.counter += 1
                if self.counter >= 5:
                    self._set_event(None)

            @override
            def _yield_coroutines(self) -> Iterator[Callable[[], Coroutine1[None]]]:
                yield partial(inc_external, self)

            @override
            def _yield_events_and_exceptions(
                self,
            ) -> Iterator[tuple[None, MaybeType[BaseException]]]:
                yield (None, CustomError)

        looper = Example(sleep_core=0.05, sleep_restart=0.05)
        with raises(TimeoutError):
            async with timeout_dur(duration=1.0):
                await looper()
        assert 4 <= looper.initializations <= 6
        assert 0 <= looper.counter <= 7
        assert 16 <= external <= 21

    async def test_with_coroutine_self_error(self) -> None:
        class CustomError(Exception): ...

        async def dummy() -> None:
            _ = await Event().wait()

        @dataclass(kw_only=True)
        class Example(InfiniteLooper[None]):
            initializations: int = 0
            counter: int = 0

            @override
            async def _initialize(self) -> None:
                self.initializations += 1
                self.counter = 0

            @override
            async def _core(self) -> None:
                self.counter += 1
                if self.counter >= 5:
                    raise CustomError

            @override
            def _yield_coroutines(self) -> Iterator[Callable[[], Coroutine1[None]]]:
                yield dummy

            @override
            def _yield_events_and_exceptions(
                self,
            ) -> Iterator[tuple[None, MaybeType[BaseException]]]:
                yield (None, CustomError)

        looper = Example(sleep_core=0.05, sleep_restart=0.05)
        with raises(TimeoutError):
            async with timeout_dur(duration=1.0):
                await looper()
        assert 3 <= looper.initializations <= 5
        assert 0 <= looper.counter <= 5

    @given(logger=just("logger") | none())
    async def test_with_coroutine_other_coroutine_error(
        self, *, logger: str | None
    ) -> None:
        class CustomError(Exception): ...

        async def dummy() -> None:
            for i in count():
                if i >= 5:
                    raise CustomError
                await sleep(0.05)

        @dataclass(kw_only=True)
        class Example(InfiniteLooper[None]):
            initializations: int = 0
            counter: int = 0

            @override
            async def _initialize(self) -> None:
                self.initializations += 1
                self.counter = 0

            @override
            async def _core(self) -> None:
                self.counter += 1

            @override
            def _yield_coroutines(self) -> Iterator[Callable[[], Coroutine1[None]]]:
                yield dummy

            @override
            def _yield_events_and_exceptions(
                self,
            ) -> Iterator[tuple[None, MaybeType[BaseException]]]:
                yield (None, CustomError)

        looper = Example(sleep_core=0.05, sleep_restart=0.05, logger=logger)
        with raises(CancelledError):
            async with timeout_dur(duration=1.0):
                await looper()
        assert 3 <= looper.initializations <= 5
        assert 1 <= looper.counter <= 6

    @given(logger=just("logger") | none())
    async def test_error_upon_initialize(self, *, logger: str | None) -> None:
        class CustomError(Exception): ...

        @dataclass(kw_only=True)
        class Example(InfiniteLooper[None]):
            @override
            async def _initialize(self) -> None:
                raise CustomError

            @override
            async def _core(self) -> None:
                raise NotImplementedError

        looper = Example(sleep_core=0.1, logger=logger)
        with raises(TimeoutError):
            async with timeout_dur(duration=0.5):
                _ = await looper()

    @given(logger=just("logger") | none())
    async def test_error_group_upon_coroutines(self, *, logger: str | None) -> None:
        class CustomError(Exception): ...

        @dataclass(kw_only=True)
        class Example(InfiniteLooper[None]):
            @override
            async def _core(self) -> None:
                raise CustomError

            @override
            def _yield_events_and_exceptions(
                self,
            ) -> Iterator[tuple[None, MaybeType[BaseException]]]:
                yield (None, CustomError)

        looper = Example(sleep_core=0.1, logger=logger)
        with raises(TimeoutError):
            async with timeout_dur(duration=0.5):
                _ = await looper()

    async def test_error_no_event_found(self) -> None:
        @dataclass(kw_only=True)
        class Example(InfiniteLooper[None]):
            counter: int = 0

            @override
            async def _initialize(self) -> None:
                self.counter = 0

            @override
            async def _core(self) -> None:
                self.counter += 1
                if self.counter >= 10:
                    self._set_event(None)

        looper = Example(sleep_core=0.1)
        with raises(InfiniteLooperError, match="'Example' does not have an event None"):
            _ = await looper()


class TestInfiniteQueueLooper:
    async def test_main(self) -> None:
        @dataclass(kw_only=True)
        class Example(InfiniteQueueLooper[None, int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_items(self, *items: int) -> None:
                self.output.update(items)

        looper = Example(sleep_core=0.05)

        async def add_items() -> None:
            for i in count():
                looper.put_items_nowait(i)
                await sleep(0.05)

        with raises(ExceptionGroup):  # noqa: PT012
            async with EnhancedTaskGroup(timeout=1.0) as tg:
                _ = tg.create_task(looper())
                _ = tg.create_task(add_items())
        assert 15 <= len(looper.output) <= 20

    @given(n=integers(1, 10))
    def test_len_and_empty(self, *, n: int) -> None:
        class Example(InfiniteQueueLooper[None, int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_items(self, *items: int) -> None:
                self.output.update(items)

        looper = Example(sleep_core=0.05)
        assert len(looper) == 0
        assert looper.empty()
        looper.put_items_nowait(*range(n))
        assert len(looper) == n
        assert not looper.empty()

    async def test_no_items(self) -> None:
        @dataclass(kw_only=True)
        class Example(InfiniteQueueLooper[None, int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_items(self, *items: int) -> None:
                self.output.update(items)

        looper = Example(sleep_core=0.05)
        with raises(TimeoutError):
            async with timeout_dur(duration=0.5):
                _ = await looper()

    async def test_run_until_empty(self) -> None:
        @dataclass(kw_only=True)
        class Example(InfiniteQueueLooper[None, int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_items(self, *items: int) -> None:
                self.output.update(items)

        looper = Example(sleep_core=0.5)

        async def add_items() -> None:
            for i in count():
                looper.put_items_nowait(i)
                await sleep(0.01)

        with raises(ExceptionGroup):  # noqa: PT012
            async with EnhancedTaskGroup(timeout=1.0) as tg:
                _ = tg.create_task(looper())
                _ = tg.create_task(add_items())

        tasks = len(looper)
        assert tasks >= 1
        await sleep(0.1)
        assert len(looper) == tasks
        await looper.run_until_empty()
        assert looper.empty()

    @given(logger=just("logger") | none())
    async def test_error_process_items(self, *, logger: str | None) -> None:
        class CustomError(Exception): ...

        @dataclass(kw_only=True)
        class Example(InfiniteQueueLooper[None, int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_items(self, *items: int) -> None:
                raise CustomError(*items)

        looper = Example(sleep_core=0.05, logger=logger)
        looper.put_items_nowait(1)
        with raises(TimeoutError):
            async with timeout_dur(duration=0.5):
                _ = await looper()

    async def test_error_infinite_queue_looper(self) -> None:
        class CustomError(Exception): ...

        @dataclass(kw_only=True)
        class Example(InfiniteQueueLooper[None, int]):
            @override
            async def _process_items(self, *items: int) -> None:
                raise CustomError(*items)

        looper = Example(sleep_core=0.1)
        looper.put_items_nowait(1)
        with raises(
            InfiniteQueueLooperError,
            match=r"'Example' encountered CustomError\(1\) whilst processing 1 item\(s\): \[1\]",
        ):
            _ = await looper._core()


class TestPutAndGetItems:
    @given(xs=lists(integers(), min_size=1), max_size=integers(1, 10) | none())
    async def test_put_then_get(self, *, xs: list[int], max_size: int | None) -> None:
        queue: Queue[int] = Queue()
        await put_items(xs, queue)
        result = await get_items(queue, max_size=max_size)
        if max_size is None:
            assert result == xs
        else:
            assert result == xs[:max_size]

    @given(xs=lists(integers(), min_size=1), max_size=integers(1, 10) | none())
    async def test_get_then_put(self, *, xs: list[int], max_size: int | None) -> None:
        queue: Queue[int] = Queue()

        async def put() -> None:
            await sleep(0.01)
            await put_items(xs, queue)

        async with TaskGroup() as tg:
            task = tg.create_task(get_items(queue, max_size=max_size))
            _ = tg.create_task(put())
        result = task.result()
        if max_size is None:
            assert result == xs
        else:
            assert result == xs[:max_size]

    async def test_empty(self) -> None:
        queue: Queue[int] = Queue()
        with raises(TimeoutError):  # noqa: PT012
            async with timeout(0.01), TaskGroup() as tg:
                _ = tg.create_task(get_items(queue))
                _ = tg.create_task(sleep(0.02))


class TestPutAndGetItemsNoWait:
    @given(xs=lists(integers(), min_size=1), max_size=integers(1, 10) | none())
    def test_main(self, *, xs: list[int], max_size: int | None) -> None:
        queue: Queue[int] = Queue()
        put_items_nowait(xs, queue)
        result = get_items_nowait(queue, max_size=max_size)
        if max_size is None:
            assert result == xs
        else:
            assert result == xs[:max_size]


class TestQueueProcessor:
    async def test_one_processor_slow_tasks(self) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)

        async with Example() as processor:

            async def add_tasks() -> None:
                for i in range(10):
                    processor.enqueue(i)
                    await sleep(0.1)

            async def run_until_empty() -> None:
                await sleep(0.5)
                await processor.run_until_empty()

            async with TaskGroup() as tg:
                _ = tg.create_task(add_tasks())
                _ = tg.create_task(run_until_empty())

            assert len(processor.output) == 10

    async def test_one_processor_slow_run(self) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)
                await sleep(0.01)

        async with Example() as processor:
            processor.enqueue(*range(10))
            await processor.run_until_empty()
            assert len(processor.output) == 10

    @given(n=integers(1, 10))
    async def test_one_processor_continually_adding(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)

        async with Example() as processor:
            for i in range(n):
                processor.enqueue(i)
                await sleep(0.01)
            assert len(processor.output) == n

    async def test_two_processors(self) -> None:
        @dataclass(kw_only=True)
        class First(QueueProcessor[int]):
            second: Second
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.second.enqueue(item)
                self.output.add(item)
                await sleep(0.1)

        @dataclass(kw_only=True)
        class Second(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)
                await sleep(0.01)

        async with Second() as second, First(second=second) as first:

            async def yield_tasks() -> None:
                first.enqueue(*range(10))
                await first.run_until_empty()

            await yield_tasks()
            assert len(first.output) == 10
            assert len(second.output) == 10

    @mark.parametrize("duration", [param(0.1), param(0.5), param(1.0), param(1.5)])
    async def test_cancellation(self, *, duration: float) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)
                await sleep(0.1)

        async with Example(duration=duration) as processor:
            processor.enqueue(*range(10))
        assert processor.output == set(range(10))

    async def test_empty(self) -> None:
        class Example(QueueProcessor[int]):
            @override
            async def _process_item(self, item: int, /) -> None:
                _ = item

        processor = Example()
        assert processor.empty()
        processor.enqueue(0)
        assert not processor.empty()

    @given(n=integers(0, 10))
    async def test_get_items_nowait(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, _: int, /) -> None:
                items = self._get_items_nowait()
                self.output.add(len(items))

        processor = Example()
        processor.enqueue(*range(n + 1))
        await processor._run()
        result = one(processor.output)
        assert result == n

    @given(n=integers(0, 10))
    async def test_len(self, *, n: int) -> None:
        class Example(QueueProcessor[int]):
            @override
            async def _process_item(self, item: int) -> None:
                _ = item

        processor = Example()
        assert len(processor) == 0
        processor.enqueue(*range(n))
        assert len(processor) == n

    @given(data=data(), texts=lists(text_ascii(min_size=1), min_size=1))
    async def test_priority_queue(self, *, data: DataObject, texts: list[str]) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[tuple[int, str]]):
            output: set[str] = field(default_factory=set)

            @override
            async def _process_item(self, item: tuple[int, str]) -> None:
                _, text = item
                self.output.add(text)

        processor = Example(queue_type=PriorityQueue)
        items = data.draw(permutations(list(enumerate(texts))))
        processor.enqueue(*items)
        await processor._run()
        result = one(processor.output)
        assert result == texts[0]


class TestUniquePriorityQueue:
    @given(data=data(), texts=lists(text_ascii(min_size=1), min_size=1, unique=True))
    async def test_main(self, *, data: DataObject, texts: list[str]) -> None:
        items = list(enumerate(texts))
        extra = data.draw(lists(sampled_from(items)))
        items_use = data.draw(permutations(list(chain(items, extra))))
        queue: UniquePriorityQueue[int, str] = UniquePriorityQueue()
        assert queue._set == set()
        for item in items_use:
            await queue.put(item)
        assert queue._set == set(texts)
        result = await get_items(queue)
        assert result == items
        assert queue._set == set()


class TestUniqueQueue:
    @given(x=lists(integers(), min_size=1))
    async def test_main(self, *, x: list[int]) -> None:
        queue: UniqueQueue[int] = UniqueQueue()
        assert queue._set == set()
        for x_i in x:
            await queue.put(x_i)
        assert queue._set == set(x)
        result = await get_items(queue)
        expected = list(unique_everseen(x))
        assert result == expected
        assert queue._set == set()


class TestSleepDur:
    @given(duration=sampled_from([0.1, 10 * MILLISECOND]))
    @settings(phases={Phase.generate})
    async def test_main(self, *, duration: Duration) -> None:
        with Timer() as timer:
            await sleep_dur(duration=duration)
        assert timer >= datetime_duration_to_timedelta(duration / 2)

    async def test_none(self) -> None:
        with Timer() as timer:
            await sleep_dur()
        assert timer <= 0.01


class TestSleepUntil:
    async def test_main(self) -> None:
        now = get_now()
        with Timer() as timer:
            await sleep_until(now + 10 * MILLISECOND)
        assert timer >= datetime_duration_to_timedelta(5 * MILLISECOND)


class TestSleepUntilRounded:
    async def test_main(self) -> None:
        await sleep_until_rounded(10 * MILLISECOND)


class TestStreamCommand:
    @skipif_windows
    async def test_main(self) -> None:
        output = await stream_command(
            'echo "stdout message" && sleep 0.1 && echo "stderr message" >&2'
        )
        await sleep(0.01)
        assert output.return_code == 0
        assert output.stdout == "stdout message\n"
        assert output.stderr == "stderr message\n"

    @skipif_windows
    async def test_error(self) -> None:
        output = await stream_command("this-is-an-error")
        await sleep(0.01)
        assert output.return_code == 127
        assert output.stdout == ""
        assert search(
            r"^/bin/sh: (1: )?this-is-an-error: (command )?not found$", output.stderr
        )


class TestTimeoutDur:
    async def test_pass(self) -> None:
        async with timeout_dur(duration=0.2):
            await sleep(0.1)

    async def test_fail(self) -> None:
        with raises(TimeoutError):
            async with timeout_dur(duration=0.05):
                await sleep(0.1)

    async def test_custom_error(self) -> None:
        class CustomError(Exception): ...

        with raises(CustomError):
            async with timeout_dur(duration=0.05, error=CustomError):
                await sleep(0.1)


if __name__ == "__main__":
    _ = run(
        stream_command('echo "stdout message" && sleep 2 && echo "stderr message" >&2')
    )
