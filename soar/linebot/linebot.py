import logging

from fastapi import FastAPI, Request, HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent, FollowEvent
from linebot.v3.webhooks.models import follow_event
from linebot.v3.webhooks.models import message_event
from linebot.v3.webhooks.models import postback_event

from soar.config import get_channel_secret, get_channel_access_token
from soar.handlers.on_follow import invoke_on_follow_handler
from soar.handlers.on_message import invoke_on_message_handler
from soar.handlers.on_post_back import invoke_on_post_back_handler
from soar.linebot.event_wrapper.on_follow_event import OnFollowEvent
from soar.linebot.event_wrapper.on_message_event import OnMessageEvent
from soar.linebot.event_wrapper.on_post_back_event import OnPostBackEvent

configuration = Configuration(access_token=get_channel_access_token())
handler = WebhookHandler(get_channel_secret())
logger = logging.getLogger(__name__)
app = FastAPI()


def register_line_bot_handlers():
    @app.post("/callback")
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
    def handle_message(event: message_event.MessageEvent):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            wrapped_on_message_event = OnMessageEvent(event, line_bot_api)
            invoke_on_message_handler(wrapped_on_message_event)

    @handler.add(PostbackEvent)
    def handle_postback(event: postback_event.PostbackEvent):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            wrapped_on_post_back_event = OnPostBackEvent(event, line_bot_api)
            invoke_on_post_back_handler(wrapped_on_post_back_event)

    @handler.add(FollowEvent)
    def handle_follow(event: follow_event.FollowEvent):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            wrapped_on_follow_event = OnFollowEvent(event, line_bot_api)
            invoke_on_follow_handler(wrapped_on_follow_event)
