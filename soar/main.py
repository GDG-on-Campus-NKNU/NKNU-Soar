import uvicorn

from soar.linebot.linebot import register_line_bot_handlers
from soar.logger import setup_logger
from soar.plugins.loader import load_plugins


def main():
    setup_logger()

    load_plugins()
    register_line_bot_handlers()

    uvicorn.run("soar.linebot.linebot:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
