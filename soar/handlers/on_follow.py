import logging

from soar.linebot.event_wrapper.on_follow_event import OnFollowEvent

__ON_FOLLOW_HANDLERS = []

logger = logging.getLogger(__name__)


def on_follow(handler_name: str):
    def decorator(func):
        logger.info(f"Registered on follow handler {handler_name}")
        __ON_FOLLOW_HANDLERS.append(func)

    return decorator


def invoke_on_follow_handler(event: OnFollowEvent):
    for handler in __ON_FOLLOW_HANDLERS:
        handler(event)
