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
    message_event.add_text_message(str(message_event.get_data_content()))
    message_event.submit_reply()


@on_follow.add_handler()
def on_follow(event: OnFollowEvent):
    event.add_text_message(f"{event.get_follower_id()} has followed")
    event.add_text_message(f"Is unblock: {event.is_unblock()}")
    event.submit_reply()


@on_message.add_handler(key="all_actions")
def all_actions(message_event: OnMessageEvent):
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
        create_uri_action("uri action", "https://github.com/GDG-on-Campus-NKNU/NKNU-Soar")
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
    message_event.add_text_message(str((message_event._json_data)))
    message_event.add_text_message(str((message_event.get_datetime_picker_action_result())))
    message_event.submit_reply()
