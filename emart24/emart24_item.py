import time

import requests
from bs4 import BeautifulSoup

from .emart24_common import write_json


def get_raw_data_html(page_index):
    req = requests.get(
        f"https://www.emart24.co.kr/goods/event?search=&page={page_index}&category_seq=&align=", verify=False)
    if req.ok:
        return req.text
    else:
        return None


def get_item_list_html(data):
    soup = BeautifulSoup(data, "html.parser")
    item_list = soup.find_all("div", "itemWrap")
    return item_list


def get_item_info(item):
    item_type = ""
    item_type_text = ""

    if item.find("span", "floatR") != None:
        item_type = item.find("span", "floatR").attrs["class"][0]

    if item_type != "":
        item_type_text = item.find("span", item_type).text

    item_title = item.find("div", "itemtitle").text.replace("\n", "")
    item_img = item.find("div", "itemImg").find("img").attrs["src"]
    item_price = item.find("a", "price").text
    item_price_off = 0
    item_dum_img = ""

    match(item_type):
        case "sale":
            item_price_off = getattr(item.find("a", "priceOff"), "text", "")
        case "dum":
            item_dum_img = item.find("div", "dumgift").find("img").attrs["src"]
        case "onepl":
            pass
        case "twopl":
            pass
        case "tripl":
            pass
        case _:
            pass

    return {
        "type": item_type,
        "type_text": item_type_text,
        "item_img": item_img,
        "title": item_title,
        "price": item_price,
        "price_off": item_price_off,
        "dum_img": item_dum_img
    }


def get_item_list_info(item_list):
    result_list = []
    for item in item_list:
        result_list.append(get_item_info(item))
    return result_list


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

    write_json(total_list, "emart24_item.json")


if __name__ == "__main__":
    run()
