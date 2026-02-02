from soar.core.plugin_event_manager import on_follow
from soar.models.event_wrapper.on_follow_event import OnFollowEvent


@on_follow.add_handler()
def on_follow(event: OnFollowEvent):
    event.add_text_message(
"""啾！我是高師校園小飛燕 🐦
由 GDG on Campus NKNU 社團所開發的 LINE Bot

點選下方選單看看現在我可以幫到你什麼～""")
    event.submit_reply()
