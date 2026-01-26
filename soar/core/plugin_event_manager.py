from dataclasses import dataclass
from typing import Callable

from soar.models.event_wrapper.base_event import BaseEvent
from soar.models.event_wrapper.keyed_event import KeyedEvent


@dataclass
class BaseHandler:
    priority: int
    handler: Callable


@dataclass
class KeyedHandler(BaseHandler):
    key: str


class KeyedEventManager:
    def __init__(self):
        self._registered_handlers: dict[str, list[KeyedHandler]] = {
            "None": []
        }

    def add_handler(self, key: str = None, priority: int = 5):
        def decorator(handler: Callable):
            parsed_key = key if key else "None"
            if parsed_key not in self._registered_handlers:
                self._registered_handlers[parsed_key] = [
                    KeyedHandler(priority, handler, key)
                ]
            else:
                self._registered_handlers[parsed_key].append(KeyedHandler(priority, handler, key))

            self._registered_handlers[parsed_key].sort(key=lambda h: h.priority, reverse=True)

        return decorator

    def invoke_handler(self, event: KeyedEvent):
        for key, handlers in self._registered_handlers.items():
            if key == event.get_key():
                for h in handlers:
                    # TODO exception handler
                    h.handler(event)
                break

        for h in self._registered_handlers["None"]:
            h.handler(event)


class BroadcastEventManager():
    def __init__(self):
        self._registered_handlers: list[BaseHandler] = []

    def add_handler(self, priority: int = 5):
        def decorator(handler: Callable):
            self._registered_handlers.append(BaseHandler(priority, handler))

            self._registered_handlers.sort(key=lambda h: h.priority, reverse=True)

        return decorator

    def invoke_handler(self, event: BaseEvent):
        for handlers in self._registered_handlers:
            # TODO exception handler
            handlers.handler(event)


on_follow = BroadcastEventManager()
on_message = KeyedEventManager()
on_postback = KeyedEventManager()
