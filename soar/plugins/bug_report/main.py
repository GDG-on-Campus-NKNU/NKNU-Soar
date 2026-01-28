from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent


@on_message.add_handler(key="問題回報")
def bug_report(event: OnMessageEvent):
    # TODO bug report
    event.add_text_message("please report bug")
    event.submit_reply()
