import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://gs25.gsretail.com",
    "Referer": "http://gs25.gsretail.com/gscvs/ko/products/event-goods"
}

PAGE_SIZE = 16


def find_in_arr(target: str, arr: list[str]):
    for one in arr:
        if one.find(target) > -1:
            return one
    return None


def get_session_token():
    res = requests.get(
        "http://gs25.gsretail.com/gscvs/ko/products/event-goods")
    soup = BeautifulSoup(res.text, "html.parser")
    cookie_list = res.headers["Set-Cookie"].split("; ")
    session = find_in_arr("JSESSIONID", cookie_list).split("=")[1]
    token = soup.find("input", attrs={"name": "CSRFToken"}).attrs['value']

    return {"token": token, "session": session}


def init_setting_data():
    session_token = get_session_token()

    return {"url": f'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search?CSRFToken={session_token["token"]}',
            "cookies": {"JSESSIONID": session_token["session"]}}


def get_raw_data_text(url, cookies, page_index, page_size):
    dataParam = {
        "pageNum": page_index, "pageSize": page_size, "searchType": "", "searchWord": "", "parameterList": "TOTAL"
    }
    req = requests.post(url=url, cookies=cookies,
                        data=dataParam, headers=HEADERS)

    if req.ok:
        return req.text
    else:
        return None


def convert_info(json_data):
    info_data = json.loads(json.loads(json_data))
    return info_data


def get_item_info(info):
    return info["results"]


def get_item_info_list(url, cookies):
    total_list = []
    page_number = 1

    while (True):
        print(page_number)
        raw_data = get_raw_data_text(url, cookies, page_number, PAGE_SIZE)
        info_data = convert_info(raw_data)
        page_item_info = get_item_info(info_data)

        if len(page_item_info) == 0:
            break

        total_list.extend(page_item_info)
        page_number += 1

    return total_list


def write_json(data, file_name):
    json_data = json.dumps(data, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)


def run():
    setting_data = init_setting_data()
    result = get_item_info_list(setting_data["url"], setting_data["cookies"])
    write_json(result, "gs_item.json")


if __name__ == "__main__":
    run()
