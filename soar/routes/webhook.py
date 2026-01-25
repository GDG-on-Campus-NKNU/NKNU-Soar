from fastapi import APIRouter, Request, HTTPException
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent, FollowEvent
from linebot.v3.webhooks.models import follow_event
from linebot.v3.webhooks.models import message_event
from linebot.v3.webhooks.models import postback_event

from soar.core.line_client import handler, configuration
from soar.core.plugin_event_manager import on_message, on_postback, on_follow
from soar.models.event_wrapper.on_follow_event import OnFollowEvent
from soar.models.event_wrapper.on_message_event import OnMessageEvent
from soar.models.event_wrapper.on_post_back_event import OnPostBackEvent
from soar.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature")

    body = (await request.body()).decode("utf-8")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.info("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature")

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def webhook_on_message(event: message_event.MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        wrapped_on_message_event = OnMessageEvent(event, line_bot_api)

        on_message.invoke_handler(wrapped_on_message_event)


@handler.add(PostbackEvent)
def webhook_on_postback(event: postback_event.PostbackEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        wrapped_on_post_back_event = OnPostBackEvent(event, line_bot_api)
        on_postback.invoke_handler(wrapped_on_post_back_event)


@handler.add(FollowEvent)
def webhook_on_follow(event: follow_event.FollowEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        wrapped_on_follow_event = OnFollowEvent(event, line_bot_api)
        on_follow.invoke_handler(wrapped_on_follow_event)
