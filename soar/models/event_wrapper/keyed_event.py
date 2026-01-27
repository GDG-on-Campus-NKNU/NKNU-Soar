from linebot.v3.webhooks.models.event import Event

from soar.models.event_wrapper.base_event import BaseEvent


class KeyedEvent(BaseEvent):
    def __init__(self, reply_token: str, original_event: Event, key: str):
        super().__init__(reply_token, original_event)
        self.__key: str = key

    def get_key(self) -> str:
        return self.__key
