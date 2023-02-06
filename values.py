import json, os.path

# работа с текстом
BG_red = '\033[41m'
BG_white = '\033[47m'
reset_style = '\033[0m'

print_line = '-' * 23


# показ данных
def print_dict_keys_and_values(some_tuple, start_enumerate=1):
    for point, action in enumerate(some_tuple, start_enumerate):
        print(f'{point}: {action}')


# работа с файлами JSON
def read_from_json(name_and_path):
    file = open(name_and_path, 'r', encoding='UTF-8')
    dictionary = json.load(file)
    file.close()
    return dictionary


def write_in_json(name_and_path, dictionary):
    with open(name_and_path, 'w', encoding='UTF-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)


# выбор информации за определенную дату
category = read_from_json(os.path.join('categories_info.json'))['category']


# категории (чтобы можно было менять при работе с программой)
category_descripton = read_from_json(os.path.join('categories_info.json'))['category_descripton']
category_habits = read_from_json(os.path.join('categories_info.json'))['category_habits']

