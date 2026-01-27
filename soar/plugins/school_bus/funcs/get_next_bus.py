from typing import Any, Callable, Tuple

from soar.models.flex_message_builder import CarouselFlexMessageBuilder
from soar.plugins.school_bus.utils.bus_card import bus_card_flex_msg_generator


def get_next_bus(
        get_now_data_func: Callable,
        get_by_index_func: Callable
) -> Tuple[Any, Any]:
    now_data = None
    next_data = None

    try:
        n = get_now_data_func()
        now_data = n["schedule"]
        try:
            next_data = get_by_index_func(n["index"] + 1)
        except Exception as e:
            if not "IndexOutOfRange" in str(e):
                raise e
    except Exception as e:
        if "NoNextBusError" not in str(e):
            raise e

    return now_data, next_data


def get_next_bus_flex_msg_content(
        now_stops: Any,
        next_stops: Any,
        from_text: str,
        to_text: str
):
    container = CarouselFlexMessageBuilder()

    container.append(bus_card_flex_msg_generator(
        now_stops,
        from_text,
        to_text,
        "NOW"
    ))

    if next_stops:
        container.append(
            bus_card_flex_msg_generator(
                next_stops,
                from_text,
                to_text,
                "NEXT"
            )
        )

    return container.build_string()
