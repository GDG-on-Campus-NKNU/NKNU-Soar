from typing import Any

from soar.models.flex_message_builder import FlexMessageBuilder
from soar.plugins.school_bus.symbol_map import SymbolMap


def bus_card_flex_msg_generator(schedule_data: Any,
                                from_text: str,
                                to_text: str,
                                time_text: str) -> FlexMessageBuilder:
    msg = FlexMessageBuilder("school_bus_container")

    msg.replace({"TIME": time_text,
                 "FROM_PLACEHOLDER": from_text,
                 "TO_PLACEHOLDER": to_text,
                 "CAUTION_TEXT": f"本車次{schedule_data["daysOfWeek"]}行駛",
                 "VEHICLE_TYPE": schedule_data["vehicleType"]
                 })

    for i in range(len(schedule_data["stations"])):
        station = schedule_data["stations"][i]
        station_flex_msg = FlexMessageBuilder("school_bus_stop")

        if "和平" in station["name"]:
            parsed_name = f"和平 - {station["name"][6:-1]} "
        else:
            parsed_name = f"燕巢 - {station["name"]} "

        parsed_name += SymbolMap.get(station["type"], "")

        station_flex_msg.replace({
            "STOP_NAME": parsed_name,
            "HOUR": f"{station["departTime"]["hour"]:0>2}",
            "MIN": f"{station["departTime"]["minute"]:0>2}",
        })

        content_index = 2 + 2 * i
        msg["body"]["contents"].insert(content_index - 1, station_flex_msg.content)

        if i != len(schedule_data["stations"]) - 1:
            l = FlexMessageBuilder("school_bus_line")
            msg["body"]["contents"].insert(content_index, l.content)

    return msg
