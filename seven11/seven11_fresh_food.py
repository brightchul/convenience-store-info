import requests
from bs4 import BeautifulSoup

from .seven11_common import (INFO_FUNCTIONS, FreshFoodType,
                             get_data_by_fresh_food_type, get_item_type_text,
                             iterate_item_info_function, json_write_file)


# fresh food 도시락/조리면 삼각김밥/김밥 샌드위치/햄버거
def get_fresh_food_html_text_data(itemType: FreshFoodType, page_size: int):
    res = requests.post(url="https://www.7-eleven.co.kr/product/dosirakNewMoreAjax.asp", data={
        "intPageSize": page_size, "pTab": itemType.value})
    if res.ok:
        return res.text
    else:
        return None


def parse_fresh_food_item_list(text: str):
    soup = BeautifulSoup(text, "html.parser")
    parent_ul = soup.select("div.dosirak_list > ul")

    if len(parent_ul) == 0:
        return []

    item_list = parent_ul[0].findChildren("li",  recursive=False)[1:-1]
    return item_list


def get_data_by_fresh_food_type(itemType: FreshFoodType):
    print(get_item_type_text(itemType))

    info_function = INFO_FUNCTIONS[itemType]

    page_size = 0

    result_list = []

    while (True):
        page_size += 150
        page_data = get_fresh_food_html_text_data(itemType, page_size)
        page_item_list = parse_fresh_food_item_list(page_data)
        page_item_list_size = len(page_item_list)

        if page_item_list_size == 0:
            break

        result_list.extend(iterate_item_info_function(
            page_item_list, itemType, info_function))

        if page_item_list_size < page_size:
            break

    return result_list


def run():
    total_list = []
    total_list.extend(get_data_by_fresh_food_type(FreshFoodType.TOTAL))

    json_write_file("seven11_fresh_food.json", total_list)


if __name__ == "__main__":
    run()
