import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import re
import json
import time

load_dotenv()

CU_SESSION = os.environ["CU_SESSION"]
 
URL = "https://cu.bgfretail.com/event/plusAjax.do"
COOKIES = {"JSESSIONID": CU_SESSION}


def get_raw_data_text(page_index):
  req = requests.post(url=URL,cookies=COOKIES,data={"pageIndex":page_index, "listType":1})
   
  if req.ok:
    return req.text
  else:
    return None



def get_prod_list_html(data):
  soup = BeautifulSoup(data, "html.parser")
  prod_list = soup.find_all("li", "prod_list")
  return prod_list


def get_item_info(item):
  item_dict= {}

  # 이미지 (img, src)
  item_dict["img"] = item.find("img").attrs["src"]

  # 제품명 
  item_dict["name"] = item.find("div", "name").text

  # 제품 가격
  item_dict["price"] = item.find("div", "price").text.replace("원","")

  # 행사 종류 (1+1, 2+1)
  item_dict["type"] = re.sub(r"\n| \n","", item.find("div","badge").text)

  # 태그 (없음, new, best)
  if item.find("div","tag").find("img") != None:
    item_dict["tag"] = (item.find("div","tag").find("img")).attrs["alt"]
  else :
    item_dict["tag"] = ""

  return item_dict

def get_item_list_info(prod_list):
  result_list = []
  for prod in prod_list:
    result_list.append(get_item_info(prod))
  return result_list



def run():
  page_index = 1
  total_list = []

  while True:
    print(page_index)
    raw_data = get_raw_data_text(page_index)
    prod_list = get_prod_list_html(raw_data)

    if len(prod_list) == 0:
      break

    item_info_list = get_item_list_info(prod_list)
    total_list.extend(item_info_list)
    page_index+=1

    time.sleep(0.1)
  
  json_data = json.dumps(total_list, ensure_ascii=False)
  with open("cu_item.json", 'w', encoding='utf-8') as file:
    file.write(json_data)


if __name__ == "__main__":  
  run()
 

