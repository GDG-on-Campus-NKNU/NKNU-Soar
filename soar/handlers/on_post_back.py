import logging

from soar.linebot.event_wrapper.on_post_back_event import OnPostBackEvent

__ON_POST_BACK_HANDLERS = {}

logger = logging.getLogger(__name__)


def on_post_back(keyword: str):
    def decorator(func):
        if keyword in __ON_POST_BACK_HANDLERS:
            logger.warning(f"Post back handler {keyword} already registered")
            return
        logger.info(f"Registered post back handler with keyword {keyword}")
        __ON_POST_BACK_HANDLERS[keyword] = func

    return decorator


def invoke_on_post_back_handler(event: OnPostBackEvent):
    prefix_handler = __ON_POST_BACK_HANDLERS.get(event.get_handler_keyword())
    if prefix_handler is not None:
        prefix_handler(event)
