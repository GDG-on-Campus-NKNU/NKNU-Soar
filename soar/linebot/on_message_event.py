from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage, QuickReply, FlexMessage, FlexContainer
from linebot.v3.webhooks.models.message_event import MessageEvent
from pydantic import StrictBool, StrictStr


class OnMessageEvent:
    def __init__(self, original_event: MessageEvent, line_bot_api: MessagingApi):
        self.__original_event = original_event
        self.__line_bot_api = line_bot_api
        self.__messages = []

    def __can_add_more_reply(self) -> bool:
        return len(self.__messages) < 5

    def get_raw_user_message(self) -> str:
        return self.__original_event.message.text

    def get_split_user_message(self) -> list[str]:
        return self.get_raw_user_message().split()

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
                replyToken=self.__original_event.reply_token,
                notificationDisabled=StrictBool(notification_disabled),
                messages=self.__messages
            )
        )
