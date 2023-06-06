import json
import time
from typing import Any, Callable

import requests
from bs4 import BeautifulSoup


def write_json(data, file_name):
    json_data = json.dumps(data, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)


def get_raw_data_html(url):
    res = requests.get(url, verify=False)
    if res.ok:
        return res.text
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


def get_item_info_from_url(url):
    raw_data = get_raw_data_html(url)
    item_list_html = get_item_list_html(raw_data)
    item_info_list = []

    if len(item_list_html) > 0:
        item_info_list = get_item_list_info(item_list_html)

    return item_info_list


def crawling_runner_by(create_request_url: Callable[[Any], str]):
    page_index = 1
    total_list = []
    prev_len = -1

    while prev_len < len(total_list):
        print(page_index)
        prev_len = len(total_list)
        url = create_request_url(page_index)
        total_list.extend(get_item_info_from_url(url))
        page_index += 1
        time.sleep(0.1)

    return total_list
