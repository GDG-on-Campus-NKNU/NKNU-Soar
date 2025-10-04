from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage, QuickReply, FlexMessage, FlexContainer
from pydantic import StrictBool, StrictStr


class BaseEvent:
    def __init__(self, reply_token: str, line_bot_api: MessagingApi):
        self.__reply_token = reply_token
        self.__line_bot_api = line_bot_api
        self.__messages = []

    def __can_add_more_reply(self) -> bool:
        return len(self.__messages) < 5

    def add_text_message(self, content: str, quick_reply: QuickReply = None, quote_token: str = None):
        if not self.__can_add_more_reply():
            raise Exception("Too many messages")
        else:
            self.__messages.append(
                TextMessage(
                    text=StrictStr(content),
                    quickReply=quick_reply,
                    quoteToken=None if quote_token is None else StrictStr(quote_token),
                )
            )

    def add_flex_message(self, content: str, alt_text: str, quick_reply: QuickReply = None):
        if not self.__can_add_more_reply():
            raise Exception("Too many messages")
        else:
            self.__messages.append(
                FlexMessage(
                    contents=FlexContainer.from_json(content),
                    quickReply=quick_reply,
                    altText=StrictStr(alt_text),
                )
            )

    def submit_reply(self, notification_disabled=False):
        self.__line_bot_api.reply_message(
            reply_message_request=ReplyMessageRequest(
                replyToken=StrictStr(self.__reply_token),
                notificationDisabled=StrictBool(notification_disabled),
                messages=self.__messages
            )
        )
