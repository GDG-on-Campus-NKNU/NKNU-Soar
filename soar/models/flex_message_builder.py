from soar.core.plugin_flex_message_manager import flex_message_manager
from soar.utils.logger import get_logger

logger = get_logger(__name__)


class FlexMessageBuilder:
    def __init__(self, key: str):
        self.__content: str = flex_message_manager.get_flex_message(key)

    def replace(self, content: dict[str, str]):
        for k, v in content.items():
            self.__content = self.__content.replace(k, v)

    def build(self):
        return self.__content
