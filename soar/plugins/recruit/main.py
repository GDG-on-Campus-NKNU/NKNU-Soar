from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent


@on_message.add_handler("我要加入")
def recruit(event: OnMessageEvent):
    # TODO
    event.add_text_message("recruit")
    event.submit_reply()
