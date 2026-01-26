import json

from soar.core.plugin_flex_message_manager import flex_message_manager
from soar.utils.logger import get_logger

logger = get_logger(__name__)


class FlexMessageBuilder:
    def __init__(self, key: str):
        self.content = json.loads(flex_message_manager.get_flex_message(key))

    def __getitem__(self, item):
        return self.content[item]

    def replace(self, replace_target: dict[str, str]):
        temp_content = json.dumps(self.content)
        for k, v in replace_target.items():
            temp_content = temp_content.replace(str(k), str(v))
        self.content = json.loads(temp_content)

    def build_string(self):
        return json.dumps(self.content)


class CarouselFlexMessageBuilder:
    def __init__(self):
        self.__content: list[FlexMessageBuilder] = []

    def append(self, content: FlexMessageBuilder):
        self.__content.append(content)

    def build_string(self):
        return json.dumps({
            "type": "carousel",
            "contents": [x.content for x in self.__content]
        })
