import json
from datetime import datetime
from typing import get_type_hints

from .. import (BaseEvent, BaseHandler)
from ...exceptions import DeserializationEventError


class EventJsonSerializerDeserializer:
    """A class for serializing and deserializing events to and from JSON
    format. This class provides methods to convert event objects to JSON
    strings and to create event objects from JSON strings.
    """

    @staticmethod
    def serialize(event: type[BaseEvent]) -> str:
        """Convert an event object to a JSON string.
        Args:
            event (BaseEvent): The event object to serialize.
        Returns:
            str: The JSON string representation of the event.
        """
        if not isinstance(event, BaseEvent):
            raise TypeError(
                f"Expected an instance of BaseEvent, got {type(event)}"
            )
        return json.dumps(
            {
                'data': {
                    'id': event.event_id,
                    'type': event.event_name,
                    'occurred_on': event.occurred_on.isoformat(),
                    'attributes': event.to_dict(),
                }
            },
            default=str,
        )

    @staticmethod
    def deserialize(event_json: str, handler: BaseHandler) -> BaseEvent:
        """Convert a JSON string to an event object.
        Args:
            event_json (str): The JSON string to deserialize.
            handler (BaseHandler): The handler to determine the event type.
        Returns:
            BaseEvent: The event object created from the JSON string.
        """
        if not isinstance(event_json, str):
            raise TypeError(
                f"Expected a JSON string, got {type(event_json)}"
            )
        try:
            json_obj = json.loads(event_json)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format: {e.msg}"
            ) from e
        if 'detail' not in json_obj or 'data' not in json_obj['detail']:
            raise ValueError(
                "Invalid JSON format: 'detail' or 'data' key not found."
            )
        data = EventJsonSerializerDeserializer._validate_and_extract_data(json_obj)  # noqa: E501
        attributes = data['attributes']
        event_id = data['id']
        occurred_on = datetime.fromisoformat(data['occurred_on'])
        event_class = EventJsonSerializerDeserializer._get_event_type_from_handler(handler)  # noqa: E501
        try:
            return event_class.from_dict(
                attributes=attributes,
                event_id=event_id,
                occurred_on=occurred_on,
            )
        except Exception as e:
            raise DeserializationEventError(handler) from e

    @staticmethod
    def _get_event_type_from_handler(handler: BaseHandler) -> type[BaseEvent]:  # noqa: E501
        """Get the event type from the handler."""
        if not isinstance(handler, BaseHandler):
            raise TypeError(
                f"Expected an instance of BaseHandler, got {type(handler)}"
            )
        cls = handler.__class__

        method = getattr(cls, 'handle', None)
        if method is None:
            raise ValueError(
                f"Handler {cls.__name__} does not have a 'handle' method.")

        type_hints = get_type_hints(method)
        event = type_hints.get('data', None)
        if not issubclass(event, BaseEvent):
            raise ValueError(
                f"Handler {cls.__name__} does not handle a valid BaseEvent type."  # noqa: E501
            )
        return event

    @staticmethod
    def _validate_and_extract_data(json_obj: dict) -> dict:
        """Validate and extract data from the detail dictionary."""
        if 'detail' not in json_obj or 'data' not in json_obj['detail']:
            raise ValueError(
                'Invalid JSON format: "detail" or "data" key not found.'  # noqa: E501
            )
        data = json_obj['detail']['data']
        missing_keys = [key for key in ['attributes',
                                        'id', 'occurred_on'] if key not in data]  # noqa: E501
        if missing_keys:
            raise ValueError(
               'Invalid JSON format: Missing keys in "data": ' + ', '.join(missing_keys)  # noqa: E501
            )
        return data
