from linebot.v3.webhooks.models.message_event import MessageEvent

from soar.models.event_wrapper.keyed_event import KeyedEvent


class OnMessageEvent(KeyedEvent):
    def __init__(self, original_event: MessageEvent):
        user_msg = original_event.message.text
        key = user_msg.split(" ")[0]

        super().__init__(original_event.reply_token, original_event, key)

    def get_raw_user_message(self) -> str:
        return self.original_event.message.text

    def get_split_user_message(self) -> list[str]:
        return self.get_raw_user_message().split()
