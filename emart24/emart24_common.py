import json


def write_json(data, file_name):
    json_data = json.dumps(data, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)
