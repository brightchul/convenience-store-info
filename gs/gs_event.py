import requests

from gs_common import convert_info, get_item_info,  init_setting_data, write_json

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://gs25.gsretail.com",
    "Referer": "http://gs25.gsretail.com/gscvs/ko/products/event-goods"
}

DOMAIN_URL = "http://gs25.gsretail.com/board/boardList"


def get_raw_data_text(url, cookies, page_index, page_size):
    dataParam = {
        "pageNum": page_index, "pageSize": page_size, "modelName": "event",
        "parameterList": "brandCode:GS25@!@eventFlag:CURRENT"
    }
    res = requests.post(url=url, cookies=cookies,
                        data=dataParam, headers=HEADERS)

    if res.ok:
        return res.text
    else:
        return None


def get_item_info_list(url, cookies):
    total_list = []
    page_number = 1

    while (True):
        print(page_number)
        raw_data = get_raw_data_text(url, cookies, page_number, 10)
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
