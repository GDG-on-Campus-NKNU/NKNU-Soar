import os

DISABLED_PLUGINS = [
    "hello_world"
]


def get_channel_access_token():
    return os.getenv("CHANNEL_ACCESS_TOKEN")


def get_channel_secret():
    return os.getenv("CHANNEL_SECRET")
