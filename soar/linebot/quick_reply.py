from linebot.v3.messaging.models import QuickReply, MessageAction, QuickReplyItem, Action
from pydantic import StrictStr


class QuickReplyWrapper:
    def __init__(self):
        self.__items = []

    def __add_item(self, action: Action, image_url: str = None):
        self.__items.append(
            QuickReplyItem(
                action=action,
                type=None,
                imageUrl=image_url,
            ),
        )

    def add_message_action(self, label: str, text: str, image_url: str = None):
        self.__add_item(MessageAction(label=StrictStr(label), text=StrictStr(text)), image_url=image_url)

    def build(self):
        return QuickReply(
            items=self.__items,
        )
