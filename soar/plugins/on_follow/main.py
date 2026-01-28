from soar.core.plugin_event_manager import on_follow
from soar.models.event_wrapper.on_follow_event import OnFollowEvent


@on_follow.add_handler()
def on_follow(event: OnFollowEvent):
    event.add_text_message("Welcome")
    event.submit_reply()
