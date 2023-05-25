from seven11_common import ItemType, get_data_by_type, json_write_file


def run():
    total_list = []
    total_list.extend(get_data_by_type(ItemType.ONE_ONE))
    total_list.extend(get_data_by_type(ItemType.TWO_ONE))
    total_list.extend(get_data_by_type(ItemType.GIFT))
    total_list.extend(get_data_by_type(ItemType.DISCOUNT))

    json_write_file("seven11_item.json", total_list)


if __name__ == "__main__":
    run()
