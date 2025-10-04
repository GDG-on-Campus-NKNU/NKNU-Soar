from soar.handlers.flex_message import build_flex_message
from soar.handlers.on_message import on_message
from soar.handlers.on_post_back import on_post_back
from soar.linebot.event_wrapper.on_message_event import OnMessageEvent
from soar.linebot.event_wrapper.on_post_back_event import OnPostBackEvent
from soar.linebot.quick_reply import QuickReplyWrapper


@on_message(prefix="hello")
def say_hello(message_event: OnMessageEvent):
    name = message_event.get_split_user_message()[1]
    message_event.add_text_message(
        "Hello, {}! ".format(name),
    )
    message_event.add_text_message(
        "How are you today?",
    )
    message_event.submit_reply()


@on_message(prefix="quick_reply")
def quick_reply_test(message_event: OnMessageEvent):
    quick_reply_wrapper = QuickReplyWrapper()
    quick_reply_wrapper.add_message_action("Flex Msg Test", "flex_example")
    quick_reply_wrapper.add_message_action("Action2", "Text2")
    message_event.add_text_message(
        "This is a quick reply test.",
        quick_reply=quick_reply_wrapper.build(),
    )
    message_event.submit_reply()


@on_message(prefix="flex_example")
def flex_example(message_event: OnMessageEvent):
    flex_message_content = build_flex_message("example", {
        "Brown Cafe": "Flex Example",
        "CALL": "Hello World"
    })
    message_event.add_flex_message(flex_message_content, "flex_example")
    message_event.submit_reply()


@on_message(prefix="post_back")
def post_back(message_event: OnMessageEvent):
    quick_reply_wrapper = QuickReplyWrapper()
    quick_reply_wrapper.add_postback_action(
        "Flex Msg Test", "123", {"a": "b"}, display_text="Display Text")
    message_event.add_text_message("Hi", quick_reply_wrapper.build())

    message_event.submit_reply()


@on_post_back(keyword="123")
def post_back_test(message_event: OnPostBackEvent):
    message_event.add_text_message(str(message_event.get_data_content()))
    message_event.submit_reply()
