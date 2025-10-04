import json

from linebot.v3.messaging import MessagingApi
from linebot.v3.webhooks.models.postback_event import PostbackEvent

from soar.linebot.event_wrapper.base_event import BaseEvent


class OnPostBackEvent(BaseEvent):
    def __init__(self, event: PostbackEvent, line_bot_api: MessagingApi):
        super().__init__(event.reply_token, line_bot_api)
        self._json_data = json.loads(event.postback.data)

    def get_handler_keyword(self) -> str | None:
        return self._json_data.get("handler_keyword")

    def get_data_content(self) -> dict:
        return self._json_data.get("content")
