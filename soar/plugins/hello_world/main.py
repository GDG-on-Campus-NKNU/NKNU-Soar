from soar.core.plugin_event_manager import on_message, on_postback, on_follow
from soar.models.event_wrapper.on_follow_event import OnFollowEvent
from soar.models.event_wrapper.on_message_event import OnMessageEvent
from soar.models.event_wrapper.on_post_back_event import OnPostBackEvent
from soar.models.flex_message_builder import FlexMessageBuilder
from soar.models.quick_reply_builder import QuickReplyBuilder


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
    quick_reply_wrapper = QuickReplyBuilder()
    quick_reply_wrapper.add_message_action("Flex Msg Test", "flex_example")
    quick_reply_wrapper.add_message_action("Action2", "Text2")
    message_event.add_text_message(
        "This is a quick reply test.",
        quick_reply=quick_reply_wrapper.build(),
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

    message_event.add_flex_message(flex_msg.build(), "flex_example")
    message_event.submit_reply()


@on_message.add_handler(key="post_back")
def post_back(message_event: OnMessageEvent):
    quick_reply_wrapper = QuickReplyBuilder()
    quick_reply_wrapper.add_postback_action(
        "Flex Msg Test", "123", {"a": "b"}, display_text="Display Text")
    message_event.add_text_message("Hi", quick_reply_wrapper.build())

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
