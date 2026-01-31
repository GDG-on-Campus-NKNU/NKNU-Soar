from fastapi import FastAPI

from soar import config
from soar.modules.analytics.db import create_table
from soar.modules.database.get_db import _get_db_handler
from soar.modules.rich_menu.loader import load_rich_menu
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
load_rich_menu()

with _get_db_handler():
    create_table()
