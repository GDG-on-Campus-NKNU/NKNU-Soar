from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, MessagingApiBlob

from soar.config import get_channel_secret, get_channel_access_token

configuration = Configuration(access_token=get_channel_access_token())
handler = WebhookHandler(get_channel_secret())
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
line_bot_api_blob = MessagingApiBlob(api_client)
