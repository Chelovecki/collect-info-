import checking_correct_data, values


def note_habits_results(category, dictionary, list_with_data):
    d, m, y = list(map(str, list_with_data))

    choise = [r for r in input('Что? ').split()]
    # проверяем на то, если ли в словарике нужный день
    if checking_correct_data.check_correct_input(category, choise):
        for r in choise:
            # это нужно, чтобы вернуться в главное меню, если я тыкнул не туда
            if category[int(r) - 1].startswith('выйти'):
                break
            # я принял решение выписывать ключ и значение
            # для следующего вывода по порядку
            dictionary[y][m][d].setdefault(r, category[int(r) - 1])

    else:
        note_habits_results(category, dictionary, list_with_data)


def add_info_in_habits(name_and_path, some_category):
    dictionary = values.read_from_json(name_and_path)

    chosen_data = input('дата на добавление:  ').split()
    chosen_data[2] = '20' + chosen_data[2]

    checking_correct_data.create_day_in_dictionary(dictionary, chosen_data)

    values.print_dict_keys_and_values(some_category)
    note_habits_results(some_category, dictionary, chosen_data)

    values.write_in_json(name_and_path, dictionary)


def show_me_data_habit(list_with_data,
                       habit_path,
                       default_mouths_dict,
                       numbered_mouths_dict):
    print(f'{values.BG_white}показать данные:{values.reset_style}')

    values.print_dict_keys_and_values(values.category, start_enumerate=0)

    dictionary = values.read_from_json(habit_path)
    action = input('Что?  ')
    print()
    try:
        match int(action):
            # вывод за один день (сегодня)
            case 1:
                print_habits_stat_day(list_with_data, dictionary, numbered_mouths_dict)

            # вывод за один день, если dd.mm.yy,
            # или же за месяц, если mm.yy (определяю сам)
            case 2:
                print(
                    '(mm yy, если за месяц; dd mm yy, если за день\nты можешь написать год без "20", т.е. "23", а не "2023"')
                list_with_data = input('введи дату:  ').split()

                match len(list_with_data):
                    case 2:
                        print_habits_stat_moth(list_with_data, dictionary, numbered_mouths_dict, default_mouths_dict)
                    case 3:
                        print_habits_stat_day(list_with_data, dictionary, numbered_mouths_dict)

            case 3:
                print_habits_stat_in_range(dictionary, default_mouths_dict, numbered_mouths_dict)

            case 0:

                raise TypeError
    except TypeError:
        None


def print_habits_stat_moth(list_with_data, dictionary, numberic_mouths_dict, default_mouths_dict):
    some_month, some_year = list_with_data
    if len(some_year) == 2:
        some_year = '20' + some_year

    if some_year in dictionary.keys():
        if some_month in dictionary[some_year].keys():
            # тут мы пишем название месяца большими буквами
            print(f'{default_mouths_dict[int(some_month)].upper()}')
            print(values.print_line)
            # чтобы все дни шли по порядку!
            days_for_mouth = sorted([int(r) for r in dictionary[some_year][some_month].keys()])
            for some_day in days_for_mouth:
                print(f'\033[4m{some_day}-е {numberic_mouths_dict[int(some_month)]}\033[0m')
                couples = [(int(place), challenge) for place, challenge in
                           dictionary[some_year][some_month][
                               str(some_day)].items()]  # int(place), чтобы потом сортировать по порядку
                for action in sorted(couples):
                    print(action[1], end='; ')
                print('\n\n')
        else:
            print('месяц еще не заполнен')
    else:
        print('год еще не заполнен')
        print('\n\n')


def print_habits_stat_day(list_with_data, dictionary, numberic_mouths_dict):
    some_day = str(list_with_data[0])
    some_month = str(list_with_data[1])
    some_year = str(list_with_data[2])

    if not (some_year.startswith('20')):
        some_year = '20' + some_year

    # int(place), чтобы потом сортировать по порядку
    couples = [(int(place), challenge) for place, challenge in
               dictionary[some_year][some_month][some_day].items()]

    if str(some_day) in dictionary[str(some_year)][str(some_month)]:
        print(f'\033[4mстата за {some_day}-е {numberic_mouths_dict[int(some_month)]}\033[0m')
        for action in sorted(couples):
            print(action[1], end='; ')
        print()

    else:
        print('день еще не заполнен')


def print_habits_stat_in_range(dictionary, default_mouths_dict, numberic_mouths_dict):
    range_data = input('за какой период?  ').split()
    begin_data = [int(r) for r in range_data[0].split('.')]
    end_data = [int(r) for r in range_data[1].split('.')]

    all_years_range = [year for year in range(int(begin_data[2]), int(end_data[2]) + 1)]
    existed_years = set(map(str, all_years_range)) & set(dictionary.keys())

    for year in existed_years:
        print('=' * 23)
        print(f'{year}-Й ГОД ')
        for month in dictionary[year].keys():
            print('-' * 20)
            print(f'{default_mouths_dict[int(month)]}:')
            for some_day in dictionary[year][month].keys():
                print(f'\033[4m{some_day}-е {numberic_mouths_dict[int(month)]}\033[0m  ', end='')
                points = [point
                          for point in dictionary[year][month][some_day].values()]
                points = '; '.join(points)
                print(f'{points}')
