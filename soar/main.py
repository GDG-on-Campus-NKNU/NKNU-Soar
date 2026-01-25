from fastapi import FastAPI

from soar import config
from soar.plugins.loader import load_plugins
from soar.routes import webhook
from soar.utils.logger import setup_logging

setup_logging(
    config.LOG_LEVEL,
    config.LOG_TO_FILE,
    config.LOG_TO_CONSOLE,
    config.LOG_JSON_FORMAT
)

app = FastAPI()
app.include_router(webhook.router)
load_plugins()
