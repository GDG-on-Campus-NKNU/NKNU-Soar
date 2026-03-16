from typing import Any

from soar.models.flex_message_builder import FlexMessageBuilder
from soar.plugins.school_bus.symbol_map import SymbolMap

def bus_card_flex_msg_generator(schedule_data: Any,
                                from_text: str,
                                to_text: str,
                                time_text: str) -> FlexMessageBuilder:
    msg = FlexMessageBuilder("school_bus_container")

    from_text = from_text[-4::]
    to_text = to_text[-4::] 

    def _campus_key(text: str) -> str | None:
        if "和平" in text:
            return "和平"
        if "燕巢" in text:
            return "燕巢"
        return None 

    from_campus = _campus_key(from_text)
    to_campus = _campus_key(to_text)

    blue = '#0367D3'#'#35385A'  
    #带入json参数
    to_hp_param = {
        "arrival_name": to_text,
        "departure_name": from_text,
        "header_font_color": "#ffffff",
        "header_background_color": '#35385A',
        "arrowhead_color" : "#FFD700",
        "timetag": time_text,
        "departure_color": blue,
        "arrival_color": "#EF454D",
        "vehical_type": schedule_data["vehicleType"][:4],
        "caution_time": schedule_data["daysOfWeek"]
        
    }

    to_yc_param = {
        "arrival_name": to_text,
        "departure_name": from_text,
        "header_font_color": "#3C3C43",
        "header_background_color": "#fdd1ce",
        "arrowhead_color" : "#3C3C43",
        "timetag": time_text,
        "departure_color": "#EF454D",
        "arrival_color": blue,
        "vehical_type": schedule_data["vehicleType"][:4],
        "caution_time": schedule_data["daysOfWeek"]
    }

#先找有几个和平stop和燕巢stop
    num_of_stop_index = {
        "和平": 0,
        "燕巢": 0
    }
    for station in schedule_data["stations"]:
        if "和平" in station["name"]:
            num_of_stop_index["和平"] += 1
        else:
            num_of_stop_index["燕巢"] += 1

# body insertion
    columns_container = msg.content["body"]["contents"][0]["contents"]
    left_column_contents = columns_container[0]["contents"]
    right_column_contents = columns_container[1]["contents"]

    for i in range(len(schedule_data["stations"])):
        station = schedule_data["stations"][i]
        
        # 准备数据
        if "(" in station["name"] and ")" in station["name"]:
             parsed_name = station["name"].split("(")[1].split(")")[0]
        else:
             parsed_name = station["name"]

        #去除多余的字
        remove_chars = "靠旁"
        parsed_name = "".join([c for c in parsed_name if c not in remove_chars])

        time = f"{station['departTime']['hour']:0>2}:{station['departTime']['minute']:0>2}"
        emoji = SymbolMap.get(station["type"], " ")

        is_peace_station = "和平" in station["name"]
        if from_campus == "和平":
            is_left_side = is_peace_station
        elif from_campus == "燕巢":
            is_left_side = not is_peace_station
        else:
            is_left_side = from_text[:2] in station["name"]

        # 选择模板和目标容器
        if is_left_side:
            station_flex_msg = FlexMessageBuilder("school_bus_stop_left")
            target_list = left_column_contents
        else:
            station_flex_msg = FlexMessageBuilder("school_bus_stop_right")
            target_list = right_column_contents

        count_key = "和平" if is_peace_station else "燕巢"

        station_flex_msg.replace({
            "time": time,
            "stop_name": parsed_name,
            "emoji": emoji
        })

        # 2. 处理连线 (添加到小卡片内部)
        if num_of_stop_index.get(count_key, 0) > 1:
            line = FlexMessageBuilder("school_bus_line")
            # 这里的 filler 逻辑保留原意
            if is_left_side:
                 line.content["contents"].insert(0, {"type": "filler"})
            else:
                 line.content["contents"].append({"type": "filler"})
            
            # 将线加入到站点卡片的内容中
            station_flex_msg.content["contents"].append(line.content)
            num_of_stop_index[count_key] -= 1
 
        # 3. 插入到大容器
        target_list.append(station_flex_msg.content)

    match to_campus:
        case "和平":
            msg.replace(to_hp_param)
        case "燕巢":
            msg.replace(to_yc_param)

    return msg

