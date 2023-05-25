from seven11_common import ItemType, get_data_by_type, json_write_file


def run():
    total_list = (get_data_by_type(ItemType.NEW_PRODUCT))

    json_write_file("seven11_new.json", total_list)


if __name__ == "__main__":
    run()
