import json


def read_from_json(name_and_path):
    filel = open(name_and_path, 'r', encoding='UTF-8')
    dictionary = json.load(filel)
    filel.close()
    return dictionary


def write_in_json(name_and_path, dictionary):
    with open(name_and_path, 'w', encoding='UTF-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)


def create_day_in_dictionary(dictionary, list_with_data):
    now_day, now_month, now_year = map(str, list_with_data)

    if now_year not in dictionary.keys():
        dictionary.setdefault(now_year, {})

    if now_month not in dictionary[now_year]:
        dictionary[now_year].setdefault(now_month, {})

    if now_day not in dictionary[now_year][now_month]:
        dictionary[now_year][now_month].setdefault(now_day, {})


def if_day_exist_in_dictionary(dictionary, list_with_data):
    some_day, some_month, some_year = map(str, list_with_data)
    if some_year not in dictionary.keys():
        return False
    if some_month not in dictionary[some_year].keys():
        return False
    if some_day not in dictionary[some_year][some_month].keys():
        return False
    return True


def check_correct_input(category, input_info):
    for symbol in input_info:
        if int(symbol) > len(
                category):  # минус использование enumerate - обращение к кортежу через индексы. тут проверка на принадлежность
            return False
        if category[int(symbol) - 1].startswith('выйти'):
            continue
    return True
