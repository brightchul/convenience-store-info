import time

import requests

from emart24.emart24_item import get_item_list_html, get_item_list_info
from .emart24_common import write_json


def get_raw_data_html(page_index):
    req = requests.get(
        f"https://www.emart24.co.kr/goods/pl?search=&page={page_index}&category_seq=&align=", verify=False)
    if req.ok:
        return req.text
    else:
        return None


def run():
    page_index = 1
    total_list = []

    while True:
        print(page_index)
        raw_data = get_raw_data_html(page_index)
        item_list_html = get_item_list_html(raw_data)

        if len(item_list_html) == 0:
            break

        item_info_list = get_item_list_info(item_list_html)
        total_list.extend(item_info_list)
        page_index += 1
        time.sleep(0.1)

    write_json(total_list, "emart24_differentiated_product.json")


if __name__ == "__main__":
    run()
