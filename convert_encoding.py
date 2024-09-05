import json


def convert_to_utf8(input_file, output_file):
    with open(input_file, 'r', encoding='windows-1251') as infile:
        data = json.load(infile)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


# Замените на соответствующие имена файлов
convert_to_utf8('fixtures/data_catalog.json', 'fixtures/data_catalog_utf8.json')
convert_to_utf8('fixtures/data_users.json', 'fixtures/data_users_utf8.json')