import re

import requests
from bs4 import BeautifulSoup

from .emart24_common import write_json

domain_url = "https://www.emart24.co.kr"
event_page_url = "https://www.emart24.co.kr/event/ing"


def get_html_from_URL(url):
    response = requests.get(url, verify=False)
    if response.ok:
        return BeautifulSoup(response.text, "html.parser")
    else:
        return None


def get_event_info_from(html):
    p_html = html.find("p")

    [start, end, title] = [
        one for one in re.split(r"\n *", p_html.text) if one]
    link = domain_url + html.attrs["href"]
    img_src = html.find("img").attrs["src"]

    return {
        "title": title,
        "link": link,
        "date_period": (start+end).replace(" ", "")
    }


def get_event_info_list_from(html):
    event_html_list = html.find_all("a", "eventWrap")
    result = []
    for one in event_html_list:
        result.append(get_event_info_from(one))
    return result


def run():
    html = get_html_from_URL(event_page_url)
    event_list = get_event_info_list_from(html)
    write_json(event_list, "emart24_event.json")


if __name__ == "__main__":
    run()
