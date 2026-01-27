from linebot.v3.webhooks.models import follow_event

from soar.models.event_wrapper.base_event import BaseEvent


class OnFollowEvent(BaseEvent):
    def __init__(self, original_event: follow_event.FollowEvent, ):
        super().__init__(original_event.reply_token, original_event)

    def is_unblock(self) -> bool:
        return bool(super().original_event.follow.is_unblocked)

    def get_follower_id(self) -> int:
        source = super().original_event.source
        return source.user_id if source else None
