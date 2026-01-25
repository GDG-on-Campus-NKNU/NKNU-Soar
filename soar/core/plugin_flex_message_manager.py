from dataclasses import dataclass

from soar.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class FlexMessage:
    key: str
    content: str


class FlexMessageManager:
    def __init__(self):
        self._flex_messages: dict[str, FlexMessage] = {}

    def add_flex_message(self, key: str, content: str):
        if key in self._flex_messages:
            logger.warning(f"Flex message already exists for {key}")
            return
        self._flex_messages[key] = FlexMessage(key, content)

    def get_flex_message(self, key: str) -> str:
        if key in self._flex_messages:
            return self._flex_messages[key].content
        else:
            logger.error(f"Flex message does not exist for {key}")
            raise KeyError


flex_message_manager = FlexMessageManager()
