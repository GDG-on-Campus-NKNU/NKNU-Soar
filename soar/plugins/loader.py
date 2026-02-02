import importlib
from pathlib import Path

from soar.config import DISABLED_PLUGINS
from soar.core.plugin_flex_message_manager import flex_message_manager
from soar.utils.logger import get_logger

logger = get_logger(__name__)

plugins_root_folder = Path(__file__).parent.resolve()


def _list_plugins():
    for item in plugins_root_folder.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            yield item


def _find_flex_message(plugin_name: str, plugin_path: Path):
    folders = [plugin_path]
    while len(folders) > 0:
        folder = folders.pop(0)
        for item in folder.iterdir():
            if item.is_dir():
                folders.append(item)
                continue
            if item.name.startswith("flex_") and item.name.endswith(".json"):
                logger.info("Found flex message {} in plugin {}".format(item.name, plugin_name))
                with open(item, "r", encoding="utf-8") as f:
                    flex_message_manager.add_flex_message("_".join(item.name.split("_")[1:])[:-5], f.read())


def load_plugins():
    for plugin in _list_plugins():
        if plugin.name in DISABLED_PLUGINS:
            logger.info("Skipping plugin {} because it is disabled in config".format(plugin.name))
            continue
        logger.info(f"Loading plugin {plugin.name}")
        if plugin.joinpath("main.py").is_file():
            importlib.import_module(f"soar.plugins.{plugin.name}.main")
            _find_flex_message(plugin.name, plugin)
        else:
            logger.warning(f"Skipping plugin {plugin.name} because main.py doesn't exist")
