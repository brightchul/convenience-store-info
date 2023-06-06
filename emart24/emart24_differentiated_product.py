from .emart24_common import crawling_runner_by, write_json


def create_request_url(page_index):
    return f"https://www.emart24.co.kr/goods/pl?search=&page={page_index}&category_seq=&align="


def run():
    total_list = crawling_runner_by(create_request_url)
    write_json(total_list, "emart24_differentiated_product.json")


if __name__ == "__main__":
    run()
