from typing import Any

from nknu_core.bindings import refresh_school_bus_data, get_hp_to_yc_bus_by_index, get_hp_to_yc_next_bus_now, \
    get_yc_to_hp_bus_by_index, get_yc_to_hp_next_bus_now, get_yc_to_hp_next_bus, get_hp_to_yc_next_bus, \
    get_yc_to_hp_schedule, get_hp_to_yc_schedule
from soar.core.plugin_event_manager import on_message, on_postback
from soar.models.event_wrapper.on_message_event import OnMessageEvent
from soar.models.event_wrapper.on_post_back_event import OnPostBackEvent
from soar.models.flex_message_builder import CarouselFlexMessageBuilder
from soar.models.quick_reply_builder import QuickReplyBuilder
from soar.modules.analytics.analytics import analytic
from soar.plugins.school_bus.funcs.get_next_bus import get_next_bus_flex_msg_content, get_next_bus
from soar.plugins.school_bus.utils.bus_card import bus_card_flex_msg_generator
from soar.utils.action_object_wrapper import create_postback_action

refresh_school_bus_data()


def __get_approximate_alt_text(schedule: Any):
    approximate_next_bus_depart_hour = schedule["stations"][0]["departTime"]["hour"]
    approximate_next_bus_depart_minute = schedule["stations"][0]["departTime"]["minute"]
    return f"下一班校車時間：{approximate_next_bus_depart_hour:0>2}:{approximate_next_bus_depart_minute:0>2}"


__directional_utils_map = {
    "往和平": {
        "from_text": "高師大 - 燕巢校區",
        "to_text": "高師大 - 和平校區",
        "total_sche_count": len(get_yc_to_hp_schedule()),
        "funcs": [
            get_yc_to_hp_next_bus_now,
            get_yc_to_hp_next_bus,
            get_yc_to_hp_bus_by_index,
        ]
    },
    "往燕巢": {
        "from_text": "高師大 - 和平校區",
        "to_text": "高師大 - 燕巢校區",
        "total_sche_count": len(get_hp_to_yc_schedule()),
        "funcs": [
            get_hp_to_yc_next_bus_now,
            get_hp_to_yc_next_bus,
            get_hp_to_yc_bus_by_index,
        ]
    }
}


@on_message.add_handler(key="下一班校車")
@analytic("下一班校車")
def next_bus(event: OnMessageEvent):
    user_msg = event.get_split_user_message()
    if len(user_msg) != 2:
        return
    direction = user_msg[1]

    if direction == "往和平":
        from_text = "高師大 - 燕巢校區"
        to_text = "高師大 - 和平校區"
        now_schedule, next_schedule = get_next_bus(
            get_yc_to_hp_next_bus_now,
            get_yc_to_hp_bus_by_index
        )
    elif direction == "往燕巢":
        from_text = "高師大 - 和平校區"
        to_text = "高師大 - 燕巢校區"
        now_schedule, next_schedule = get_next_bus(
            get_hp_to_yc_next_bus_now,
            get_hp_to_yc_bus_by_index
        )
    else:
        return

    if now_schedule is None:
        event.add_text_message("沒有車了")
        event.submit_reply()
        return

    flex_msg = get_next_bus_flex_msg_content(
        now_schedule,
        next_schedule,
        from_text,
        to_text
    )

    event.add_flex_message(flex_msg, __get_approximate_alt_text(now_schedule))
    event.submit_reply()


@on_postback.add_handler("乘車規劃")
@analytic("乘車規劃")
def bus_schedule(event: OnPostBackEvent):
    direction = event.get_data_content().get("direction")

    first_sche = None
    first_sche_index = None
    second_sche = None
    from_text = __directional_utils_map[direction]["from_text"]
    to_text = __directional_utils_map[direction]["to_text"]

    search_hint_text_msg: str | None = None

    if event.get_data_content().get("index"):
        # search by index
        func = __directional_utils_map[direction]["funcs"][2]
        first_sche_index = event.get_data_content()["index"][0]
        first_sche = func(first_sche_index)
        if len(event.get_data_content()["index"]) == 2:
            second_sche = func(event.get_data_content()["index"][1])

    else:
        # search by time
        time = event.get_datetime_picker_action_result().datetime
        first_func = __directional_utils_map[direction]["funcs"][1]
        second_func = __directional_utils_map[direction]["funcs"][2]

        try:
            now_data = first_func(
                time.year,
                time.month,
                time.day,
                time.hour,
                time.minute,
            )
            first_sche_index = now_data["index"]
            first_sche = now_data["schedule"]
            try:
                second_sche = second_func(first_sche_index + 1)
            except Exception as e:
                if not "IndexOutOfRange" in str(e):
                    raise e
        except Exception as e:
            if "NoNextBusError" in str(e):
                event.add_text_message("沒車了")
                event.submit_reply()
                return
            raise e

        search_hint_text_msg = f"查詢 {time.year}年{time.month}月{time.day}號{time.hour}點{time.minute}分 最近的校車"

    container = CarouselFlexMessageBuilder()

    now_card = bus_card_flex_msg_generator(
        first_sche,
        from_text,
        to_text,
        f"#{first_sche_index + 1}"
    )

    container.append(now_card)

    if second_sche:
        container.append(
            bus_card_flex_msg_generator(
                second_sche,
                from_text,
                to_text,
                f"#{first_sche_index + 2}"
            )
        )

    if search_hint_text_msg:
        event.add_text_message(search_hint_text_msg)

    quick_reply_builder = QuickReplyBuilder()

    if first_sche_index != 0:
        previous_index = list(range(first_sche_index - 1,
                                    max(first_sche_index - 3, -1), -1))[::-1]
        quick_reply_builder.add_option(
            create_postback_action("乘車規劃",
                                   {
                                       "index": previous_index,
                                       "direction": direction},
                                   "上一頁")
        )
    if first_sche_index < __directional_utils_map[direction]["total_sche_count"] - 1:
        next_index = list(range(first_sche_index + 2,
                                min(first_sche_index + 4, __directional_utils_map[direction]["total_sche_count"])))

        quick_reply_builder.add_option(
            create_postback_action("乘車規劃",
                                   {
                                       "index": next_index,
                                       "direction": direction,
                                   },
                                   "下一頁")
        )

    event.add_flex_message(container.build_string(),
                           __get_approximate_alt_text(first_sche),
                           quick_reply_builder.build()
                           )

    event.submit_reply()
