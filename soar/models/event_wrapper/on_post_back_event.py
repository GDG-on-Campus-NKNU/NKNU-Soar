import json
from dataclasses import dataclass
from datetime import datetime

from linebot.v3.webhooks.models.postback_event import PostbackEvent

from soar.models.event_wrapper.keyed_event import KeyedEvent


@dataclass
class DatetimePickerActionResult:
    mode: str
    format: str
    result_str: str
    datetime: datetime


class OnPostBackEvent(KeyedEvent):
    def __init__(self, original_event: PostbackEvent):
        self._json_param = original_event.postback.params
        self._json_data = json.loads(original_event.postback.data)
        key = self._json_data.get("handler_key")

        super().__init__(original_event.reply_token, original_event, key)

    def get_handler_key(self) -> str | None:
        return self._json_data.get("handler_key")

    def get_data_content(self) -> dict:
        return self._json_data.get("content")

    def get_params(self) -> dict:
        return self._json_param

    def get_datetime_picker_action_result(self) -> DatetimePickerActionResult | None:
        if not self._json_data["is_datetime_picker"]:
            return None
        time_mode = self._json_data["datetime_picker_mode"]
        time_format = self._json_data["datetime_picker_format"]
        result = self._json_param.get(time_mode)
        return DatetimePickerActionResult(time_mode, time_format, result, datetime.strptime(result, time_format))
