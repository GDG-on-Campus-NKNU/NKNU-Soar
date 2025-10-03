import logging

__FLEX_MESSAGES = {}

logger = logging.getLogger(__name__)


def register_flex_message(name: str, content: str):
    if name in __FLEX_MESSAGES:
        logger.warning("FlexMessage {} already registered".format(name))
    else:
        logger.info("Registering flex message {}".format(name))
        __FLEX_MESSAGES[name] = content


def build_flex_message(name, replace: dict):
    if name not in __FLEX_MESSAGES:
        raise Exception("FlexMessage {} not registered".format(name))

    content = __FLEX_MESSAGES[name]

    for k, v in replace.items():
        content = content.replace(k, v)

    return content
