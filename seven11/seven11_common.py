import requests
import json

from enum import Enum
from typing import Callable
from bs4 import BeautifulSoup


DOMAIN = "https://www.7-eleven.co.kr"


class ItemType(Enum):
    ONE_ONE = 1
    TWO_ONE = 2
    GIFT = 3
    DISCOUNT = 4
    PB = 5
    NEW_PRODUCT = 8


def get_item_type_text(item_type: ItemType):
    match(item_type):
        case ItemType.ONE_ONE: return "1+1"
        case ItemType.TWO_ONE: return "2+1"
        case ItemType.GIFT: return "gift"
        case ItemType.DISCOUNT: return "discount"
        case ItemType.PB: return "pb"
        case ItemType.NEW_PRODUCT: return "new"


# page1는 13개, 그 이후 페이지는 10개씩
# page1은 page_size가 14이상일 경우 무조건 13개만 나옴
# page2이상은 page_size가 홈페이지값인 10이 아닌 값이 되면 홈페이지와 동일한 순서로 응답이 오지 않으며 훨씬 느림
def get_html_text_data(item_type: ItemType, page_size: int, current_page: int):
    res = requests.post(url="https://www.7-eleven.co.kr/product/listMoreAjax.asp", data={
                        "intCurrPage": current_page, "intPageSize": page_size, "pTab": item_type.value})
    if res.ok:
        return res.text
    else:
        return None


def iterate_item_info_function(item_list, itemType: ItemType, info_function: Callable):
    result_list = []
    for item in item_list:
        item_info = info_function(item, itemType)
        result_list.append(item_info)
    return result_list


def get_tag_info(item):
    tag_element_list = item.find("ul", "tag_list_01").find_all("li")
    return list(map(lambda x: x.text.replace("\n", ""), tag_element_list))


def get_item_img(item):
    src = item.find("img").attrs["src"]
    return f'{DOMAIN}{src}'


def get_item_name(item):
    name_html = item.find("div", "name")
    if name_html == None:
        name_html = item.find("dd", "txt_product")
    return name_html.text


def get_item_price(item):
    price_html = item.find("div", "price")
    if price_html == None:
        price_html = item.find("dd", "price_list")
    return price_html.text.replace("\n", "")


def parse_item_list(text: str):
    soup = BeautifulSoup(text, "html.parser")
    item_list = soup.findChildren("li", recursive=False)[:-1]
    return item_list


def get_info_gift(item, itemType: ItemType):
    [origin, gift] = item.findAll("div", "pic_product")

    return {
        "type": get_item_type_text(itemType),
        "tag_info": get_tag_info(item),
        "item": {
            "img": get_item_img(origin),
            "name": get_item_name(origin),
            "price": get_item_price(origin)
        },
        "gift": {
            "img": get_item_img(gift),
            "name": get_item_name(gift),
            "price": get_item_price(gift)
        }
    }


def get_basic_info_product(item, itemType: ItemType):
    return {"type": get_item_type_text(itemType),
            "tag_info": get_tag_info(item),
            "img": get_item_img(item),
            "name": get_item_name(item),
            "price": get_item_price(item)}


INFO_FUNCTIONS = {
    ItemType.ONE_ONE:  get_basic_info_product,
    ItemType.TWO_ONE:  get_basic_info_product,
    ItemType.GIFT:  get_info_gift,
    ItemType.DISCOUNT:  get_basic_info_product,
    ItemType.PB: get_basic_info_product,
    ItemType.NEW_PRODUCT: get_basic_info_product
}


def json_write_file(file_name, list_data):
    json_data = json.dumps(list_data, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)


def get_data_by_type(itemType: ItemType):
    print(get_item_type_text(itemType))
    page_number = 1
    info_function = INFO_FUNCTIONS[itemType]

    # 처음엔 13개
    page1_data = get_html_text_data(itemType, 13, page_number)
    page1_item_list = parse_item_list(page1_data)

    result_list = iterate_item_info_function(
        page1_item_list, itemType, info_function)

    # 이후엔 10개씩만
    while (True):
        page_number += 1
        print(page_number)
        page_data = get_html_text_data(itemType, 10, page_number)
        page_item_list = parse_item_list(page_data)
        if len(page_item_list) == 0:
            break

        result_list.extend(iterate_item_info_function(
            page_item_list, itemType, info_function))

    return result_list
