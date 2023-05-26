import json
import re

import requests
from bs4 import BeautifulSoup

from cu_common import write_json

URL = "https://cu.bgfretail.com/product/pbAjax.do"


def get_raw_data_text(url, page_index, searchgubun):
    req = requests.post(
        url=url,
        data={"pageIndex": page_index,
              "gdIdx": 0,
              "searchCondition": "setA",
              "searchgubun": searchgubun})

    if req.ok:
        return req.text
    else:
        return None


def get_prod_list_html(data):
    soup = BeautifulSoup(data, "html.parser")
    prod_list = soup.find_all("li", "prod_list")
    return prod_list


def get_item_info(item):
    item_dict = {}

    # 이미지 (img, src)
    item_dict["img"] = item.find("img").attrs["src"]

    # 제품명
    item_dict["name"] = item.find("div", "name").text

    # 제품 가격
    item_dict["price"] = item.find("div", "price").text.replace("원", "")

    # 행사 종류 (1+1, 2+1)
    item_dict["type"] = re.sub(r"\n| \n", "", item.find("div", "badge").text)

    # 태그 (없음, new, best)
    if item.find("div", "tag").find("img") != None:
        item_dict["tag"] = (item.find("div", "tag").find("img")).attrs["alt"]
    else:
        item_dict["tag"] = ""

    return item_dict


def get_item_list_info(prod_list):
    result_list = []
    for prod in prod_list:
        result_list.append(get_item_info(prod))
    return result_list


# PBG 는 PB상품
# CUG 는 CU 단독 상품
def get_item_info_list(searchgubun):
    page_index = 1
    total_list = []

    while True:
        print(f'{searchgubun} == {page_index}')
        raw_data = get_raw_data_text(URL, page_index, searchgubun)
        prod_list = get_prod_list_html(raw_data)

        if len(prod_list) == 0:
            break

        item_info_list = get_item_list_info(prod_list)
        total_list.extend(item_info_list)
        page_index += 1

    return total_list


def run():
    result = []
    result.extend(get_item_info_list("PBG"))
    result.extend(get_item_info_list("CUG"))

    write_json(result, "cu_pb_item.json")


if __name__ == "__main__":
    run()
