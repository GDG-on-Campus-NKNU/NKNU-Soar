import logging

from fastapi import FastAPI, Request, HTTPException
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from soar.config import get_channel_secret, get_channel_access_token
from soar.linebot.on_message_event import OnMessageEvent
from soar.handlers.on_message import invoke_on_message_handler

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
    def handle_message(event):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            wrapped_on_message_event = OnMessageEvent(event, line_bot_api)
            invoke_on_message_handler(wrapped_on_message_event)

    @handler.add
    def handle_postback(event):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
