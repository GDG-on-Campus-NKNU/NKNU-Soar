import importlib
from pathlib import Path

from linebot.v3.messaging import RichMenuResponse

from soar.config import DEFAULT_RICH_MENU, RECREATE_RICH_MENU
from soar.core.line_client import line_bot_api, line_bot_api_blob
from soar.modules.rich_menu.rich_menu_manager import rich_menu_manager
from soar.utils.logger import get_logger

__root = Path(__file__).parent.resolve()
__menu_folder = __root.joinpath("menus")

logger = get_logger(__name__)


def load_rich_menu():
    if RECREATE_RICH_MENU:
        logger.warning("You have set the RECREATE_RICH_MENU to true, so all the rich menus will be recreated.")

    created_menus = __get_created_rich_menu()
    menus = __list_rich_menu()

    for menu_name in menus:
        parsed_name = f"nknu-{menu_name}"

        if RECREATE_RICH_MENU and created_menus.get(parsed_name):
            line_bot_api.delete_rich_menu(created_menus.get(parsed_name).rich_menu_id)
            logger.debug(f"Deleted rich menu. ID: {created_menus.get(parsed_name).rich_menu_id}")

        if not RECREATE_RICH_MENU and created_menus.get(parsed_name):
            rich_menu_manager.add_rich_menu(menu_name, created_menus[parsed_name].rich_menu_id)
            continue

        # upload missing rich menu
        module = importlib.import_module(f"soar.modules.rich_menu.menus.{menu_name}")
        create_rich_menu_req = module.main()
        create_rich_menu_req.name = parsed_name

        menu_id = line_bot_api.create_rich_menu(create_rich_menu_req).rich_menu_id
        logger.debug(f"Created rich menu. ID: {menu_id}")
        with open(__menu_folder.joinpath(f"{menu_name}.jpg"), "rb") as f:
            line_bot_api_blob.set_rich_menu_image(rich_menu_id=menu_id,
                                                  body=bytearray(f.read()),
                                                  _headers={'Content-Type': 'image/jpeg'})

        rich_menu_manager.add_rich_menu(menu_name, menu_id)

    line_bot_api.set_default_rich_menu(rich_menu_manager.get_rich_menu_id(DEFAULT_RICH_MENU))


def __get_created_rich_menu() -> dict[str, RichMenuResponse]:
    m = line_bot_api.get_rich_menu_list().richmenus
    r = {}
    for menu in m:
        logger.debug(f"Found created rich menu. Name: {menu.name} ID: {menu.rich_menu_id}")
        r[menu.name] = menu
    return r


def __list_rich_menu() -> list[str]:
    r = []
    for f in __menu_folder.iterdir():
        if f.is_dir() or f.suffix != ".py" or f.name.startswith("_"):
            continue

        r.append(f.name[:-3])

    return r
