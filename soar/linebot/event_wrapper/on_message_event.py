from linebot.v3.messaging import MessagingApi
from linebot.v3.webhooks.models.message_event import MessageEvent

from soar.linebot.event_wrapper.base_event import BaseEvent


class OnMessageEvent(BaseEvent):
    def __init__(self, original_event: MessageEvent, line_bot_api: MessagingApi):
        super().__init__(original_event.reply_token, line_bot_api)
        self.__original_event = original_event

    def get_raw_user_message(self) -> str:
        return self.__original_event.message.text

    def get_split_user_message(self) -> list[str]:
        return self.get_raw_user_message().split()
