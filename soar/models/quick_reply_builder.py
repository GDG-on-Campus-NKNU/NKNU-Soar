from linebot.v3.messaging.models import QuickReply, QuickReplyItem, Action


class QuickReplyBuilder:
    def __init__(self):
        self.__items = []

    def add_option(self, action: Action, image_url: str = None):
        self.__items.append(
            QuickReplyItem(
                action=action,
                type=None,
                imageUrl=image_url,
            ),
        )

    def build(self):
        return QuickReply(
            items=self.__items,
        )
