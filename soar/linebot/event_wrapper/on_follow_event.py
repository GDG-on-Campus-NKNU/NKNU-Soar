from linebot.v3.messaging import MessagingApi
from linebot.v3.webhooks.models import follow_event

from soar.linebot.event_wrapper.base_event import BaseEvent


class OnFollowEvent(BaseEvent):
    def __init__(self, event: follow_event.FollowEvent, line_bot_api: MessagingApi):
        super().__init__(event.reply_token, line_bot_api)
        self.__event = event

    def is_unblock(self) -> bool:
        return bool(self.__event.follow.is_unblocked)

    def get_follower_id(self) -> int:
        return self.__event.source.user_id
