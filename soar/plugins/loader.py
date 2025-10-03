import importlib
import logging
import os

from soar.handlers.flex_message import register_flex_message

logger = logging.getLogger(__name__)


def _list_plugins():
    for item in os.listdir(os.path.dirname(__file__)):
        if os.path.isdir(os.path.join(os.path.dirname(__file__), item)) and not item.startswith("_"):
            yield item


def find_flex_message(plugin_folder: str):
    for item in os.listdir(os.path.join(os.path.dirname(__file__), plugin_folder)):
        if item.startswith("flex_") and item.endswith(".json"):
            logger.info("Found flex message {} in plugin {}".format(item, plugin_folder))
            with open(os.path.join(os.path.dirname(__file__), plugin_folder, item), "r") as f:
                register_flex_message(item.split("_")[1][:-5], f.read())


def load_plugins():
    for plugin in _list_plugins():
        logger.info(f"Loading plugin {plugin}")
        importlib.import_module(f"soar.plugins.{plugin}.main")

        find_flex_message(plugin)
