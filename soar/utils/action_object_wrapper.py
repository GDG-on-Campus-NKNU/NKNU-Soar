import json
from datetime import datetime
from typing import Any, Literal

from linebot.v3.messaging import PostbackAction, MessageAction, URIAction, DatetimePickerAction, RichMenuSwitchAction, \
    AltUri
from pydantic import StrictStr


def __create_postback_data(handler_key: str,
                           content: Any,
                           is_datetime_picker: bool = False,
                           datetime_picker_mode: str = None,
                           datetime_picker_format: str = None):
    return json.dumps({
        "handler_key": handler_key,
        "content": content,
        "is_datetime_picker": is_datetime_picker,
        "datetime_picker_mode": datetime_picker_mode,
        "datetime_picker_format": datetime_picker_format,
    })


def create_postback_action(
        postback_handler_key: str,
        postback_content: Any,
        label: str,
        display_text: str = None,
        input_option: str = None,
        fill_in_text: str = None
):
    return PostbackAction(label=StrictStr(label),
                          data=__create_postback_data(postback_handler_key, postback_content),
                          displayText=None if display_text is None else StrictStr(display_text),
                          inputOption=None if input_option is None else StrictStr(input_option),
                          fillInText=None if fill_in_text is None else StrictStr(fill_in_text),
                          )


def create_message_action(label: str, text: str):
    return MessageAction(label=StrictStr(label), text=StrictStr(text))


def create_uri_action(label: str, uri: str, alt_uri_desktop: str = None):
    return URIAction(label=StrictStr(label), uri=StrictStr(uri),
                     altUri=AltUri(desktop=alt_uri_desktop) if alt_uri_desktop else None)


def create_datetime_picker_action(
        postback_handler_key: str,
        postback_content: Any,
        label: str,
        mode: Literal["date", "time", "datetime"],
        initial: datetime = None,
        max_datetime: datetime = None,
        min_datetime: datetime = None,
):
    if mode == "date":
        time_format = "%Y-%m-%d"
    elif mode == "time":
        time_format = "%H:%M"
    else:
        time_format = "%Y-%m-%dT%H:%M"

    return DatetimePickerAction(
        label=StrictStr(label),
        data=__create_postback_data(postback_handler_key, postback_content, True, mode, time_format),
        mode=StrictStr(mode),
        initial=StrictStr(initial.strftime(time_format)) if initial else None,
        max=StrictStr(max_datetime.strftime(time_format)) if max_datetime else None,
        min=StrictStr(min_datetime.strftime(time_format)) if min_datetime else None,
    )


def create_rich_menu_switch_action(
        postback_handler_key: str,
        postback_content: Any,
        label: str,
        rich_menu_alas_id: str,
):
    return RichMenuSwitchAction(
        label=StrictStr(label),
        richMenuAliasId=rich_menu_alas_id,
        data=__create_postback_data(postback_handler_key, postback_content),
    )
