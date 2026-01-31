from fastapi import APIRouter, Request, HTTPException
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent, FollowEvent
from linebot.v3.webhooks.models import follow_event
from linebot.v3.webhooks.models import message_event
from linebot.v3.webhooks.models import postback_event

from soar.core.line_client import handler
from soar.core.plugin_event_manager import on_message, on_postback, on_follow
from soar.models.event_wrapper.on_follow_event import OnFollowEvent
from soar.models.event_wrapper.on_message_event import OnMessageEvent
from soar.models.event_wrapper.on_post_back_event import OnPostBackEvent
from soar.modules.database.get_db import _get_db_handler
from soar.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature")

    body = (await request.body()).decode("utf-8")
    try:
        with _get_db_handler():
            handler.handle(body, signature)
    except InvalidSignatureError:
        logger.info("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature")

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def webhook_on_message(event: message_event.MessageEvent):
    wrapped_on_message_event = OnMessageEvent(event)
    on_message.invoke_handler(wrapped_on_message_event)


@handler.add(PostbackEvent)
def webhook_on_postback(event: postback_event.PostbackEvent):
    wrapped_on_post_back_event = OnPostBackEvent(event)
    on_postback.invoke_handler(wrapped_on_post_back_event)


@handler.add(FollowEvent)
def webhook_on_follow(event: follow_event.FollowEvent):
    wrapped_on_follow_event = OnFollowEvent(event)
    on_follow.invoke_handler(wrapped_on_follow_event)
