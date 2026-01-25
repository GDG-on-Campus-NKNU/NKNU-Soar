from linebot.v3.messaging import MessagingApi
from linebot.v3.webhooks.models.event import Event

from soar.models.event_wrapper.base_event import BaseEvent


class KeyedEvent(BaseEvent):
    def __init__(self, reply_token: str, line_bot_api: MessagingApi, original_event: Event, key: str):
        super().__init__(reply_token, line_bot_api, original_event)
        self.__key: str = key

    def get_key(self) -> str:
        return self.__key
