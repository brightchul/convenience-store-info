from dataclasses import dataclass
import requests
import json
from bs4 import BeautifulSoup


def find_in_arr(target: str, arr: list[str]):
    for one in arr:
        if one.find(target) > -1:
            return one
    return None


def convert_info(json_data):
    info_data = json.loads(json.loads(json_data))
    return info_data


def get_item_info(info):
    return info["results"]


def write_json(data, file_name):
    json_data = json.dumps(data, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)


@dataclass
class SessionToken:
    session: str
    token: str


def get_session_token() -> SessionToken:
    res = requests.get(
        "http://gs25.gsretail.com/gscvs/ko/products/event-goods")
    soup = BeautifulSoup(res.text, "html.parser")
    cookie_list = res.headers["Set-Cookie"].split("; ")
    session = find_in_arr("JSESSIONID", cookie_list).split("=")[1]
    token = soup.find("input", attrs={"name": "CSRFToken"}).attrs['value']

    return SessionToken(session, token)


def init_setting_data(url: str):
    session_token = get_session_token()

    return {"url": f'{url}?CSRFToken={session_token.token}',
            "cookies": {"JSESSIONID": session_token.session}}
