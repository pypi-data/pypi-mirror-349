import boto3
import asyncio
import logging
import traceback

from .. import CONFIG
from ..core import (EventHandlerRegistry, BaseHandler,
                    EventJsonSerializerDeserializer, AsyncHandler,
                    SyncHandler, BaseDeduplication)
from ..exceptions import (HandlerExecutionError, DeserializationEventError)


class SQSDispatcher:
    """Dispatcher for handling events from AWS SQS queues.
    This class is responsible for polling SQS queues, deserializing events,
    executing handlers, and managing deduplication of events.
    """  # noqa: E501

    def __init__(self, deduplication: BaseDeduplication = None):
        """
        Initialize the SQSDispatcher.
        Args:
            deduplication (BaseDeduplication, optional): An instance of a deduplication strategy.
                If provided, it will be used to check for duplicate events.
                Defaults to None. Can be an instance of `RedisDeduplication`
                or any other class that implements the `BaseDeduplication` interface.. Example:
                    >>> from events_bus.core.infrastructure.redis_deduplication import RedisDeduplication
                    >>> deduplication = RedisDeduplication(url='redis://localhost:6379/0')
                    >>> dispatcher = SQSDispatcher(deduplication=deduplication)
        """  # noqa: E501
        self.client = boto3.client('sqs',
                                   region_name=CONFIG.AWS_REGION_NAME,
                                   endpoint_url=CONFIG.AWS_CLIENT_URL)
        self._stop_event = asyncio.Event()
        self.deduplication = deduplication

    def stop(self):
        self._stop_event.set()

    async def start(self):
        """Start the SQS dispatcher.
        This method initializes the SQS client and starts polling the queues
        registered in the `EventHandlerRegistry`. It creates a separate task
        for each queue to handle events concurrently.
        """  # noqa: E501
        for queue_url, handler in EventHandlerRegistry.get_handlers().items():
            task = asyncio.create_task(self._poll_queue(queue_url, handler))  # noqa: E501
            task.add_done_callback(self._handle_task_exception)

    def consume(self):
        """Consume messages from the SQS queues.
        """
        for queue_url, handler in EventHandlerRegistry.get_handlers().items():
            task = asyncio.create_task(self._execute(queue_url, handler))
            task.add_done_callback(self._handle_task_exception)

    def _handle_task_exception(self, task: asyncio.Task):
        try:
            exc = task.exception()
            if exc:
                logging.error(
                    f"An error occurred in task {task.get_name()}: {exc}")
        except asyncio.CancelledError:
            logging.info(f"The task {task.get_name()} was cancelled.")

    async def _poll_queue(self, queue_url, handler: BaseHandler):  # noqa: E501
        while not self._stop_event.is_set():
            await self._execute(
                queue_url=queue_url,
                handler=handler
            )

    async def _execute(self, queue_url, handler: BaseHandler):
        event_name = None
        try:
            response = await asyncio.to_thread(
                self.client.receive_message,
                QueueUrl=queue_url,
                MaxNumberOfMessages=CONFIG.MAX_NUMBER_OF_MESSAGES,
                WaitTimeSeconds=CONFIG.WAIT_TIME_SECONDS,
                VisibilityTimeout=CONFIG.VISIBILITY_TIMEOUT,
            )

            for msg in response.get('Messages', []):
                event_name = await self._process_message(queue_url, msg, handler)   # noqa: E50
                await asyncio.sleep(CONFIG.SLEEP_BETWEEN_MESSAGES_SECONDS)
        except (Exception, HandlerExecutionError, DeserializationEventError):  # noqa: E501
            logging.error(traceback.format_exc())
            logging.error(
                f"""Error processing message from queue {queue_url}\n 'EventName': {event_name}"""  # noqa: E501
            )
            await asyncio.sleep(CONFIG.ERROR_SLEEP_SECONDS)  # noqa: E501

    async def _execute_handler(self, handler: BaseHandler, event, event_name: str):  # noqa: E501
        try:
            if isinstance(handler, AsyncHandler):
                await handler.handle(event)
            elif isinstance(handler, SyncHandler):
                await asyncio.to_thread(handler.handle, event)
            else:
                raise TypeError(
                    f"Handler {handler.__class__.__name__} is not a valid handler type."  # noqa: E501
                )
        except Exception as e:
            raise HandlerExecutionError(
                handler=handler,
                event_name=event_name
            ) from e

    async def _process_message(self,
                               queue_url: str,
                               msg: dict,
                               handler: BaseHandler) -> str:
        """Process a single message from the SQS queue."""
        event = EventJsonSerializerDeserializer.deserialize(
            event_json=msg['Body'],
            handler=handler
        )
        event_name = event.event_name

        if self.deduplication and self.deduplication.is_duplicate(event.event_id):  # noqa: E501
            logging.info(
                f"Duplicate event detected: {event.event_id} for handler {handler.__class__.__name__}"  # noqa: E501
            )
            return
        await self._execute_handler(handler, event, event_name)

        if self.deduplication:
            self.deduplication.mark_as_processed(event.event_id)

        await asyncio.to_thread(
            self.client.delete_message,
            QueueUrl=queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )
        return event_name
