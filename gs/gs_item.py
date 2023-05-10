import os
from dotenv import load_dotenv
import requests
import json
import time


load_dotenv()

GS_TOKEN = os.environ["GS_TOKEN"]
GS_SESSION = os.environ["GS_SESSION"]


URL = f'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search?CSRFToken={GS_TOKEN}'
COOKIES = {"JSESSIONID": GS_SESSION}
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://gs25.gsretail.com",
    "Referer": "http://gs25.gsretail.com/gscvs/ko/products/event-goods"
}


def get_raw_data_text(page_index, page_size):
    dataParam = {
        "pageNum": page_index, "pageSize": page_size, "searchType": "", "searchWord": "", "parameterList": "TOTAL"
    }
    req = requests.post(url=URL, cookies=COOKIES,
                        data=dataParam, headers=HEADERS)

    if req.ok:
        return req.text
    else:
        return None


def convert_info(json_data):
    info_data = json.loads(json.loads(json_data))
    return info_data


def get_item_info(info):
    print(info)
    return info["results"]


def get_number_of_pages(info):
    return info["pagination"]["numberOfPages"]


def run():

    total_list = []

    raw_data = get_raw_data_text(1, 16)
    info_data = convert_info(raw_data)
    page1_item_info = get_item_info(info_data)
    total_list.extend(page1_item_info)

    max_page_number = get_number_of_pages(info_data)

    for page_number in range(2, max_page_number):
        raw_data = get_raw_data_text(page_number, 16)
        info_data = convert_info(raw_data)
        page_item_info = get_item_info(info_data)
        total_list.extend(page_item_info)
        time.sleep(0.1)

    json_data = json.dumps(total_list, ensure_ascii=False)
    with open("gs_item.json", 'w', encoding='utf-8') as file:
        file.write(json_data)


if __name__ == "__main__":
    run()
