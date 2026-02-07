"""Hello World 插件範例模組。

這個模組展示了如何處理各種 LINE 訊息事件，包括：
- 文字訊息回應
- Quick Reply (快速回覆)
- Flex Message (彈性訊息)
- Postback 事件
- DateTime Picker (日期時間選擇器)
- Follow (加入好友) 事件
"""

from datetime import datetime

from soar.core.plugin_event_manager import on_message, on_postback, on_follow
from soar.models.event_wrapper.on_follow_event import OnFollowEvent
from soar.models.event_wrapper.on_message_event import OnMessageEvent
from soar.models.event_wrapper.on_post_back_event import OnPostBackEvent
from soar.models.flex_message_builder import FlexMessageBuilder
from soar.models.quick_reply_builder import QuickReplyBuilder
from soar.utils.action_object_wrapper import create_message_action, create_postback_action, create_uri_action, \
    create_datetime_picker_action


@on_message.add_handler(key="hello")
def say_hello(message_event: OnMessageEvent):
    """處理以 'hello' 為開頭的訊息事件。

    根據使用者輸入的內容進行回應。
    如果使用者只輸入 'hello'，則回覆 'Hello World'。
    如果輸入 'hello <名字>'，則回覆 'Hello, <名字>! How are you today?'。

    Args:
        message_event: 包含訊息事件相關資訊的 OnMessageEvent 物件。
    """
    if len(message_event.get_split_user_message()) < 2:
        message_event.add_text_message("Hello World")
        message_event.submit_reply()
        return

    name = message_event.get_split_user_message()[1]
    message_event.add_text_message(
        "Hello, {}! ".format(name),
    )
    message_event.add_text_message(
        "How are you today?",
    )
    message_event.submit_reply()


@on_message.add_handler(key="quick_reply")
def quick_reply_test(message_event: OnMessageEvent):
    """展示 Quick Reply 功能。

    建立一個包含 Flex Message 測試和普通文字動作的 Quick Reply 選單，
    並發送給使用者。

    Args:
        message_event: 包含訊息事件相關資訊的 OnMessageEvent 物件。
    """
    flex_msg_test = create_message_action(
        "Flex Msg Test", "flex_example")
    action2 = create_message_action("Action2", "Text2")

    quick_reply_builder = QuickReplyBuilder()
    quick_reply_builder.add_option(flex_msg_test)
    quick_reply_builder.add_option(action2)

    message_event.add_text_message(
        "This is a quick reply test.",
        quick_reply=quick_reply_builder.build(),
    )
    message_event.submit_reply()


@on_message.add_handler(key="flex_example")
def flex_example(message_event: OnMessageEvent):
    """展示 Flex Message 功能。

    讀取名為 'example' 的 Flex Message 模板，替換其中的文字內容，
    並發送給使用者。

    Args:
        message_event: 包含訊息事件相關資訊的 OnMessageEvent 物件。
    """
    flex_msg = FlexMessageBuilder("example")

    flex_msg.replace(
        {
            "Brown Cafe": "Flex Example",
            "CALL": "Hello World"
        }
    )

    message_event.add_flex_message(flex_msg.build_string(), "flex_example")
    message_event.submit_reply()


@on_message.add_handler(key="post_back")
def post_back(message_event: OnMessageEvent):
    """展示 Postback Action 功能。

    建立一個帶有 Postback 動作的 Quick Reply，
    當使用者點擊時會觸發 Postback 事件。

    Args:
        message_event: 包含訊息事件相關資訊的 OnMessageEvent 物件。
    """
    quick_reply_builder = QuickReplyBuilder()
    quick_reply_builder.add_option(
        create_postback_action(
            "123", {"a": "b"}, "Flex Msg Test", display_text="Display Text"
        )
    )
    message_event.add_text_message("Hi", quick_reply_builder.build())

    message_event.submit_reply()


@on_postback.add_handler(key="123")
def post_back_test(message_event: OnPostBackEvent):
    """處理 Postback 事件 (key='123')。

    當使用者觸發 key 為 '123' 的 Postback 事件時，
    回覆該事件攜帶的資料內容。

    Args:
        message_event: 包含 Postback 事件相關資訊的 OnPostBackEvent 物件。
    """
    message_event.add_text_message(str(message_event.get_data_content()))
    message_event.submit_reply()


@on_follow.add_handler()
def on_follow(event: OnFollowEvent):
    """處理加入好友 (Follow) 事件。

    當使用者加入官方帳號為好友時觸發，回覆使用者的 ID 以及是否為解除封鎖狀態。

    Args:
        event: 包含 Follow 事件相關資訊的 OnFollowEvent 物件。
    """
    event.add_text_message(f"{event.get_follower_id()} has followed")
    event.add_text_message(f"Is unblock: {event.is_unblock()}")
    event.submit_reply()


@on_message.add_handler(key="all_actions")
def all_actions(message_event: OnMessageEvent):
    """展示所有類型的 Action 功能。

    建立一個包含多種 Action 的 Quick Reply 選單：
    - Postback Action
    - Message Action
    - URI Action
    - Datetime Picker Action (日期、時間、日期時間)

    Args:
        message_event: 包含訊息事件相關資訊的 OnMessageEvent 物件。
    """
    quick_reply_builder = QuickReplyBuilder()
    quick_reply_builder.add_option(
        create_postback_action(
            "123", {"a": "b"}, "postback action"
        )
    )
    quick_reply_builder.add_option(
        create_message_action("message action", "NKNU_SOAR")
    )
    quick_reply_builder.add_option(
        create_uri_action(
            "uri action", "https://github.com/GDG-on-Campus-NKNU/NKNU-Soar")
    )
    quick_reply_builder.add_option(
        create_datetime_picker_action(
            "datetime_picker_test",
            {},
            "dt picker action",
            "datetime",
            initial=datetime.now(),
            min_datetime=datetime.now(),
            max_datetime=datetime.now(),
        )
    )
    quick_reply_builder.add_option(
        create_datetime_picker_action(
            "datetime_picker_test",
            {},
            "t picker action",
            "time",
            initial=datetime.now(),
            min_datetime=datetime.now(),
            max_datetime=datetime.now(),
        )
    )
    quick_reply_builder.add_option(
        create_datetime_picker_action(
            "datetime_picker_test",
            {},
            "d picker action",
            "date",
            initial=datetime.now(),
            min_datetime=datetime.now(),
            max_datetime=datetime.now(),
        )
    )
    message_event.add_text_message(
        "This is quick reply test.",
        quick_reply_builder.build(),
    )
    message_event.submit_reply()


@on_postback.add_handler(key="datetime_picker_test")
def datetime_picker_test(message_event: OnPostBackEvent):
    """處理 DateTime Picker 的 Postback 事件。

    當使用者透過 DateTime Picker 選擇時間後觸發，
    回覆原始 JSON 資料以及解析後的結果。

    Args:
        message_event: 包含 Postback 事件相關資訊的 OnPostBackEvent 物件。
    """
    message_event.add_text_message(str((message_event._json_data)))
    message_event.add_text_message(
        str((message_event.get_datetime_picker_action_result())))
    message_event.submit_reply()
