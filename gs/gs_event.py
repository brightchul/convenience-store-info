from .gs_common import (HEADERS, convert_info, get_item_info, get_raw_data_text,
                        init_setting_data, write_json)

DOMAIN_URL = "http://gs25.gsretail.com/board/boardList"


def create_event_data_param(page_index, page_size):
    return {
        "pageNum": page_index, "pageSize": page_size, "modelName": "event",
        "parameterList": "brandCode:GS25@!@eventFlag:CURRENT"
    }


def get_item_info_list(url, cookies):
    total_list = []
    page_number = 1

    while (True):
        print(page_number)
        data_param = create_event_data_param(page_number, 10)
        raw_data = get_raw_data_text(url, HEADERS, cookies, data_param)
        info_data = convert_info(raw_data)
        page_item_info = get_item_info(info_data)

        if len(page_item_info) == 0:
            break

        total_list.extend(page_item_info)
        page_number += 1

    return total_list


def run():
    setting_data = init_setting_data(DOMAIN_URL)
    result = get_item_info_list(setting_data["url"], setting_data["cookies"])
    write_json(result, "gs_event.json")


if __name__ == "__main__":
    run()
