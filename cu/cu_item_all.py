import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup

from .cu_common import write_json

URL = "https://cu.bgfretail.com/product/productAjax.do"


"""
searchMainCategory
10 : 간편식사
20 : 즉석조리
30 : 과자류
40 : 아이스크림
50 : 식품
60 : 음료
70 : 생활용품
"""
MAIN_CATEGORIES_NUM = [10, 20, 30, 40, 50, 60, 70]


def get_main_category_name(category: str):
    match(category):
        case 10: return "간편식사"
        case 20: return "즉석조리"
        case 30: return "과자류"
        case 40: return "아이스크림"
        case 50: return "식품"
        case 60: return "음료"
        case 70: return "생활용품"


async def get_raw_data_text(session, url, page_index, search_main_category, list_type=0):
    async with session.post(
        url=url,
        data={
            "pageIndex": str(page_index),
            "searchMainCategory": str(search_main_category),
            "searchSubCategory": "",
            "listType": str(list_type),
            "searchCondition": "setA",
            "searchUseYn": "N",
            "gdIdx": "0",
            "codeParent": str(search_main_category),
            "user_id": "",
            "search1": "",
            "search2": "",
            "searchKeyword": "",
        },
    ) as response:
        if response.status == 200:
            return await response.text()
        else:
            return None


def get_prod_list_html(data):
    soup = BeautifulSoup(data, "html.parser")
    prod_list = soup.find_all("li", "prod_list")
    return prod_list


def get_item_info(item):
    item_dict = {}

    # 제품 아이디
    item_dict["productId"] = re.findall(
        r"\d+", item.find("div", "prod_img").attrs['onclick'])[0]

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


async def get_item_info_list(main_category):
    async with aiohttp.ClientSession() as session:
        page_index = 1
        total_list = []

        while True:
            print(get_main_category_name(main_category), page_index)
            raw_data = await get_raw_data_text(
                session, URL, page_index, main_category
            )
            prod_list = get_prod_list_html(raw_data)

            if len(prod_list) == 0:
                break

            item_info_list = get_item_list_info(prod_list)
            total_list.extend(item_info_list)
            page_index += 1

        return total_list


async def run():
    # 7 catogories and almost 161 pages
    tasks = [
        asyncio.create_task(get_item_info_list(main_category)) for main_category in MAIN_CATEGORIES_NUM
    ]

    results = await asyncio.gather(*tasks)
    flattened_result = []

    for result in results:
        flattened_result.extend(result)

    write_json(flattened_result, "cu_item_all.json")


if __name__ == "__main__":
    asyncio.run(run())
