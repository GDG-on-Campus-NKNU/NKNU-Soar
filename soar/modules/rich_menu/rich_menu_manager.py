from soar.core.line_client import line_bot_api


class RichMenuManager:
    def __init__(self):
        self.__menus: dict[str, str] = {}

    def add_rich_menu(self, name: str, menu_id: str):
        self.__menus[name] = menu_id

    def get_rich_menu_id(self, name: str):
        return self.__menus[name]

    def link_menu_to_user(self, menu_name: str, user_id: str):
        line_bot_api.link_rich_menu_id_to_user(user_id, self.__menus[menu_name])


rich_menu_manager = RichMenuManager()
