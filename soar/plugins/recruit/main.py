from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent


@on_message.add_handler("我要加入")
def recruit(event: OnMessageEvent):
    event.add_text_message(
"""嗨嗨～我是 高師校園小飛燕 ✨
目前由 GDG on Campus NKNU 社團進行維護

如果你想參與、想一起打造更酷的校園服務 🐦
或有任何想法或創意 💡 
都歡迎加入我們！

不用擔心沒經驗 
只要有心就能一起飛 💪

加入我們👇
https://linktr.ee/gdscnknu
""")
    event.submit_reply()
