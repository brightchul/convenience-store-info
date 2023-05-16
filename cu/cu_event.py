from bs4 import BeautifulSoup
import requests
import re
import json

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


def get_starting_html(html):
    h3_arr = html.find_all("h3")
    event_h3 = find_html_arr("5월 이벤트", h3_arr)
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


def write_json(data, file_name):
    json_data = json.dumps(data, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)


def run():
    event_list = get_event_list()
    write_json(event_list, "cu_event.json")


if __name__ == "__main__":
    run()
