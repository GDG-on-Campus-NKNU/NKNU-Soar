from nknu_core.bindings import refresh_school_bus_data, get_hp_to_yc_bus_by_index, get_hp_to_yc_next_bus_now, \
    get_yc_to_hp_bus_by_index, get_yc_to_hp_next_bus_now
from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent
from soar.plugins.school_bus.funcs.get_next_bus import get_next_bus_flex_msg_content, get_next_bus

refresh_school_bus_data()


@on_message.add_handler(key="下一班校車")
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

    approximate_next_bus_depart_hour = now_schedule["stations"][0]["departTime"]["hour"]
    approximate_next_bus_depart_minute = now_schedule["stations"][0]["departTime"]["minute"]
    alt_text = f"下一班校車時間：{approximate_next_bus_depart_hour:0>2}:{approximate_next_bus_depart_minute:0>2}"

    flex_msg = get_next_bus_flex_msg_content(
        now_schedule,
        next_schedule,
        from_text,
        to_text
    )

    event.add_flex_message(flex_msg, alt_text)
    event.submit_reply()
