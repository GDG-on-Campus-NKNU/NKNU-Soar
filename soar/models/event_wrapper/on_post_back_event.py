import json

from linebot.v3.messaging import MessagingApi
from linebot.v3.webhooks.models.postback_event import PostbackEvent

from soar.models.event_wrapper.keyed_event import KeyedEvent


class OnPostBackEvent(KeyedEvent):
    def __init__(self, original_event: PostbackEvent, line_bot_api: MessagingApi):
        self._json_data = json.loads(original_event.postback.data)
        key = self._json_data.get("handler_keyword")

        super().__init__(original_event.reply_token, line_bot_api, original_event, key)

    def get_handler_keyword(self) -> str | None:
        return self._json_data.get("handler_keyword")

    def get_data_content(self) -> dict:
        return self._json_data.get("content")
