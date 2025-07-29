import asyncio
import logging

from collections.abc import AsyncGenerator
from typing import cast

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import (
    Event,
    EventConsumer,
    EventQueue,
    InMemoryQueueManager,
    QueueManager,
    TaskQueueExists,
)
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.server.tasks import (
    PushNotifier,
    ResultAggregator,
    TaskManager,
    TaskStore,
)
from a2a.types import (
    InternalError,
    Message,
    MessageSendConfiguration,
    MessageSendParams,
    PushNotificationConfig,
    Task,
    TaskIdParams,
    TaskNotFoundError,
    TaskPushNotificationConfig,
    TaskQueryParams,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from a2a.utils.telemetry import SpanKind, trace_class


logger = logging.getLogger(__name__)


@trace_class(kind=SpanKind.SERVER)
class DefaultRequestHandler(RequestHandler):
    """Default request handler for all incoming requests."""

    _running_agents: dict[str, asyncio.Task]

    def __init__(
        self,
        agent_executor: AgentExecutor,
        task_store: TaskStore,
        queue_manager: QueueManager | None = None,
        push_notifier: PushNotifier | None = None,
    ) -> None:
        self.agent_executor = agent_executor
        self.task_store = task_store
        self._queue_manager = queue_manager or InMemoryQueueManager()
        self._push_notifier = push_notifier
        # TODO: Likely want an interface for managing this, like AgentExecutionManager.
        self._running_agents = {}
        self._running_agents_lock = asyncio.Lock()

    async def on_get_task(self, params: TaskQueryParams) -> Task | None:
        """Default handler for 'tasks/get'."""
        task: Task | None = await self.task_store.get(params.id)
        if not task:
            raise ServerError(error=TaskNotFoundError())
        return task

    async def on_cancel_task(self, params: TaskIdParams) -> Task | None:
        """Default handler for 'tasks/cancel'."""
        task: Task | None = await self.task_store.get(params.id)
        if not task:
            raise ServerError(error=TaskNotFoundError())

        task_manager = TaskManager(
            task_id=task.id,
            context_id=task.contextId,
            task_store=self.task_store,
            initial_message=None,
        )
        result_aggregator = ResultAggregator(task_manager)

        queue = await self._queue_manager.tap(task.id)
        if not queue:
            queue = EventQueue()

        await self.agent_executor.cancel(
            RequestContext(
                None,
                task_id=task.id,
                context_id=task.contextId,
                task=task,
            ),
            queue,
        )
        # Cancel the ongoing task, if one exists.
        if producer_task := self._running_agents.get(task.id):
            producer_task.cancel()

        consumer = EventConsumer(queue)
        result = await result_aggregator.consume_all(consumer)
        if isinstance(result, Task):
            return result

        raise ServerError(
            error=InternalError(message='Agent did not result valid response')
        )

    async def _run_event_stream(
        self, request: RequestContext, queue: EventQueue
    ) -> None:
        await self.agent_executor.execute(request, queue)
        queue.close()

    async def on_message_send(
        self, params: MessageSendParams
    ) -> Message | Task:
        """Default handler for 'message/send' interface."""
        task_manager = TaskManager(
            task_id=params.message.taskId,
            context_id=params.message.contextId,
            task_store=self.task_store,
            initial_message=params.message,
        )
        task: Task | None = await task_manager.get_task()
        if task:
            task = task_manager.update_with_message(params.message, task)
            if self.should_add_push_info(params):
                assert isinstance(self._push_notifier, PushNotifier)
                assert isinstance(
                    params.configuration, MessageSendConfiguration
                )
                assert isinstance(
                    params.configuration.pushNotificationConfig,
                    PushNotificationConfig,
                )
                await self._push_notifier.set_info(
                    task.id, params.configuration.pushNotificationConfig
                )
        request_context = RequestContext(
            params,
            task.id if task else None,
            task.contextId if task else None,
            task,
        )
        task_id = cast(str, request_context.task_id)
        # Always assign a task ID. We may not actually upgrade to a task, but
        # dictating the task ID at this layer is useful for tracking running
        # agents.
        queue = await self._queue_manager.create_or_tap(task_id)
        result_aggregator = ResultAggregator(task_manager)
        # TODO: to manage the non-blocking flows.
        producer_task = asyncio.create_task(
            self._run_event_stream(
                request_context,
                queue,
            )
        )
        await self._register_producer(task_id, producer_task)

        consumer = EventConsumer(queue)
        producer_task.add_done_callback(consumer.agent_task_callback)

        interrupted = False
        try:
            (
                result,
                interrupted,
            ) = await result_aggregator.consume_and_break_on_interrupt(consumer)
            if not result:
                raise ServerError(error=InternalError())
        finally:
            if interrupted:
                # TODO: Track this disconnected cleanup task.
                asyncio.create_task(
                    self._cleanup_producer(producer_task, task_id)
                )
            else:
                await self._cleanup_producer(producer_task, task_id)

        return result

    async def on_message_send_stream(
        self, params: MessageSendParams
    ) -> AsyncGenerator[Event]:
        """Default handler for 'message/stream'."""
        task_manager = TaskManager(
            task_id=params.message.taskId,
            context_id=params.message.contextId,
            task_store=self.task_store,
            initial_message=params.message,
        )
        task: Task | None = await task_manager.get_task()

        if task:
            task = task_manager.update_with_message(params.message, task)

            if self.should_add_push_info(params):
                assert isinstance(self._push_notifier, PushNotifier)
                assert isinstance(
                    params.configuration, MessageSendConfiguration
                )
                assert isinstance(
                    params.configuration.pushNotificationConfig,
                    PushNotificationConfig,
                )
                await self._push_notifier.set_info(
                    task.id, params.configuration.pushNotificationConfig
                )
        else:
            queue = EventQueue()
        result_aggregator = ResultAggregator(task_manager)
        request_context = RequestContext(
            params,
            task.id if task else None,
            task.contextId if task else None,
            task,
        )
        task_id = cast(str, request_context.task_id)
        queue = await self._queue_manager.create_or_tap(task_id)
        producer_task = asyncio.create_task(
            self._run_event_stream(
                request_context,
                queue,
            )
        )
        await self._register_producer(task_id, producer_task)

        try:
            consumer = EventConsumer(queue)
            producer_task.add_done_callback(consumer.agent_task_callback)
            async for event in result_aggregator.consume_and_emit(consumer):
                if isinstance(event, Task) and task_id != event.id:
                    logger.warning(
                        f'Agent generated task_id={event.id} does not match the RequestContext task_id={task_id}.'
                    )
                    try:
                        created_task: Task = event
                        await self._queue_manager.add(created_task.id, queue)
                        task_id = created_task.id
                    except TaskQueueExists:
                        logging.info(
                            'Multiple Task objects created in event stream.'
                        )
                    if (
                        self._push_notifier
                        and params.configuration
                        and params.configuration.pushNotificationConfig
                    ):
                        await self._push_notifier.set_info(
                            created_task.id,
                            params.configuration.pushNotificationConfig,
                        )
                if self._push_notifier and task_id:
                    latest_task = await result_aggregator.current_result
                    if isinstance(latest_task, Task):
                        await self._push_notifier.send_notification(latest_task)
                yield event
        finally:
            await self._cleanup_producer(producer_task, task_id)

    async def _register_producer(self, task_id, producer_task) -> None:
        async with self._running_agents_lock:
            self._running_agents[task_id] = producer_task

    async def _cleanup_producer(self, producer_task, task_id) -> None:
        await producer_task
        await self._queue_manager.close(task_id)
        async with self._running_agents_lock:
            self._running_agents.pop(task_id, None)

    async def on_set_task_push_notification_config(
        self, params: TaskPushNotificationConfig
    ) -> TaskPushNotificationConfig:
        """Default handler for 'tasks/pushNotificationConfig/set'."""
        if not self._push_notifier:
            raise ServerError(error=UnsupportedOperationError())

        task: Task | None = await self.task_store.get(params.taskId)
        if not task:
            raise ServerError(error=TaskNotFoundError())

        await self._push_notifier.set_info(
            params.taskId,
            params.pushNotificationConfig,
        )

        return params

    async def on_get_task_push_notification_config(
        self, params: TaskIdParams
    ) -> TaskPushNotificationConfig:
        """Default handler for 'tasks/pushNotificationConfig/get'."""
        if not self._push_notifier:
            raise ServerError(error=UnsupportedOperationError())

        task: Task | None = await self.task_store.get(params.id)
        if not task:
            raise ServerError(error=TaskNotFoundError())

        push_notification_config = await self._push_notifier.get_info(params.id)
        if not push_notification_config:
            raise ServerError(error=InternalError())

        return TaskPushNotificationConfig(
            taskId=params.id, pushNotificationConfig=push_notification_config
        )

    async def on_resubscribe_to_task(
        self, params: TaskIdParams
    ) -> AsyncGenerator[Event]:
        """Default handler for 'tasks/resubscribe'."""
        task: Task | None = await self.task_store.get(params.id)
        if not task:
            raise ServerError(error=TaskNotFoundError())

        task_manager = TaskManager(
            task_id=task.id,
            context_id=task.contextId,
            task_store=self.task_store,
            initial_message=None,
        )

        result_aggregator = ResultAggregator(task_manager)

        queue = await self._queue_manager.tap(task.id)
        if not queue:
            raise ServerError(error=TaskNotFoundError())

        consumer = EventConsumer(queue)
        async for event in result_aggregator.consume_and_emit(consumer):
            yield event

    def should_add_push_info(self, params: MessageSendParams) -> bool:
        return bool(
            self._push_notifier
            and params.configuration
            and params.configuration.pushNotificationConfig
        )
