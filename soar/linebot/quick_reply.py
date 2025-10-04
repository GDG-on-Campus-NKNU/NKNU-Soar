import json

from linebot.v3.messaging import PostbackAction
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

    def add_postback_action(self, label: str, data_handler_keyword: str, data_content: dict, display_text: str = None,
                            input_option: str = None, fill_in_text: str = None, image_url: str = None):
        """

        :param label:
        :param data_handler_keyword:
        :param data_content:
        :param display_text: User 點 post back action 後 會傳的訊息
        :param input_option:
        :param fill_in_text:
        :param image_url:
        :return:
        """
        self.__add_item(PostbackAction(label=StrictStr(label),
                                       data=json.dumps(
                                           {
                                               "handler_keyword": data_handler_keyword,
                                               "content": data_content,
                                           }
                                       ),
                                       displayText=None if display_text is None else StrictStr(display_text),
                                       inputOption=None if input_option is None else StrictStr(input_option),
                                       fillInText=None if fill_in_text is None else StrictStr(fill_in_text),
                                       ), image_url=image_url)

    def build(self):
        return QuickReply(
            items=self.__items,
        )
