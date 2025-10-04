import logging

from soar.linebot.event_wrapper.on_message_event import OnMessageEvent

__ON_MESSAGE_HANDLERS = {}

logger = logging.getLogger(__name__)


def on_message(prefix: str):
    def decorator(func):
        if prefix in __ON_MESSAGE_HANDLERS:
            logger.warning(f"Message handler {prefix} already registered")
            return
        logger.info(f"Registered message handler with prefix {prefix}")
        __ON_MESSAGE_HANDLERS[prefix] = func

    return decorator


def invoke_on_message_handler(event: OnMessageEvent):
    prefix_handler = __ON_MESSAGE_HANDLERS.get(event.get_split_user_message()[0])
    if prefix_handler is not None:
        prefix_handler(event)
