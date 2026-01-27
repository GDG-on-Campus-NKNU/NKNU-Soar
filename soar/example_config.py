import os

DISABLED_PLUGINS = [
    "hello_word"
]

DEFAULT_RICH_MENU = "school_bus"
RECREATE_RICH_MENU = False

LOG_LEVEL: str = "INFO"
LOG_TO_FILE: bool = False
LOG_TO_CONSOLE: bool = True
LOG_JSON_FORMAT: bool = False


def get_channel_access_token():
    return os.getenv("CHANNEL_ACCESS_TOKEN")


def get_channel_secret():
    return os.getenv("CHANNEL_SECRET")
