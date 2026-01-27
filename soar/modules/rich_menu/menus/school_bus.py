from linebot.v3.messaging import RichMenuRequest, RichMenuSize, RichMenuArea, RichMenuBounds

from soar.utils.action_object_wrapper import create_message_action, create_datetime_picker_action


def main():
    width = 2500
    height = 1683
    option_width = width // 3
    option_height = height // 2

    return RichMenuRequest(
        size=RichMenuSize(width=width, height=height),
        selected=True,
        chatBarText="選單",
        areas=[
            # col 1
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=0, y=0, width=option_width, height=option_height
                ),
                action=create_message_action("", "下一班校車 往燕巢")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=0, y=option_height, width=option_width, height=option_height
                ),
                action=create_message_action("", "下一班校車 往和平")
            ),
            # col 2
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=option_width, y=0, width=option_width, height=option_height
                ),
                action=create_datetime_picker_action("乘車規劃", {"direction": "往燕巢"}, "", "datetime")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=option_width, y=option_height, width=option_width, height=option_height
                ),
                action=create_datetime_picker_action("乘車規劃", {"direction": "往和平"}, "", "datetime")
            ),
            # col 3
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=2 * option_width, y=0, width=option_width, height=option_height
                ),
                action=create_message_action("", "問題回報")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=2 * option_width, y=option_height, width=option_width, height=option_height
                ),
                action=create_message_action("", "我要加入")
            ),
        ]
    )
