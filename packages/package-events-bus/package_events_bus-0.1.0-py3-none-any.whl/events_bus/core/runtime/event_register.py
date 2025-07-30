from .. import BaseHandler


class EventHandlerRegistry:
    """Registry for event handlers.
    This class is responsible for registering event handlers and
    providing access to them.
    """
    _registry: dict[str, BaseHandler] = {}

    @classmethod
    def register(cls, queue_url: str, handler: BaseHandler):
        """Register an event handler with the registry.
        Args:
            queue_url (str): The URL of the queue to which the handler is
            associated.
            handler (BaseHandler): The event handler to register.
        """
        cls._registry[queue_url] = handler

    @classmethod
    def get_handlers(cls) -> dict[str, BaseHandler]:
        """Get all registered event handlers.
        Returns:
            dict[str, BaseHandler]: A dictionary mapping queue URLs to
            their associated event handlers.
        """
        return cls._registry
