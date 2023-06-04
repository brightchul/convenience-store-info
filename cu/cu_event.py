import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from .cu_common import write_json

URL = "https://linktr.ee/cu_official"


def find_html_arr(target, html_arr):
    for one in html_arr:
        if target in one.text:
            return one
    return None


def get_html_from_URL(url):
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text, "html.parser")
    else:
        return None


def get_current_month():
    return datetime.now().month


def get_starting_html(html):
    current_month = get_current_month()
    h3_arr = html.find_all("h3")
    event_h3 = find_html_arr(f"{current_month}월 이벤트", h3_arr)
    event_h3_parent_div = event_h3.parent
    return event_h3_parent_div


def get_event_info_from(html):
    if html.find("h3") != None:
        return None

    event_a_html = html.find("a")

    event_info = {}
    event_info["title"] = event_a_html.text
    event_info["link"] = href = event_a_html.attrs["href"]

    if "pocketcu.co.kr/event" in href:
        content_html = get_html_from_URL(href)
        if content_html != None:
            event_info["date_period"] = re.sub(
                r"\r|\n|\t", "", content_html.find("p", "date").text)

    return event_info


def get_event_list():
    soup = get_html_from_URL(URL)
    prev_div = get_starting_html(soup)

    event_list = []

    while (True):
        current_div = prev_div.nextSibling
        event_info = get_event_info_from(current_div)
        if event_info == None:
            break
        event_list.append(event_info)
        prev_div = current_div

    return event_list


def run():
    event_list = get_event_list()
    write_json(event_list, "cu_event.json")


if __name__ == "__main__":
    run()
