import importlib
import os

from soar.config import DISABLED_PLUGINS
from soar.core.plugin_flex_message_manager import flex_message_manager
from soar.utils.logger import get_logger

logger = get_logger(__name__)


def _list_plugins():
    for item in os.listdir(os.path.dirname(__file__)):
        if os.path.isdir(os.path.join(os.path.dirname(__file__), item)) and not item.startswith("_"):
            yield item


def _find_flex_message(plugin_folder: str):
    for item in os.listdir(os.path.join(os.path.dirname(__file__), plugin_folder)):
        if item.startswith("flex_") and item.endswith(".json"):
            logger.info("Found flex message {} in plugin {}".format(item, plugin_folder))
            with open(os.path.join(os.path.dirname(__file__), plugin_folder, item), "r", encoding="utf-8") as f:
                flex_message_manager.add_flex_message("_".join(item.split("_")[1:])[:-5], f.read())


def load_plugins():
    for plugin in _list_plugins():
        if plugin in DISABLED_PLUGINS:
            logger.info("Skipping plugin {} because it is disabled in config".format(plugin))
            continue
        logger.info(f"Loading plugin {plugin}")
        if os.path.isfile(os.path.join(os.path.dirname(__file__), plugin, "main.py")):
            importlib.import_module(f"soar.plugins.{plugin}.main")
            _find_flex_message(plugin)
        else:
            logger.warning(f"Skipping plugin {plugin} because main.py doesn't exist")
