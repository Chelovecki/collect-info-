import checking_correct_data, values
from datetime import datetime


def write_desc_in_dict(category, dictionary, list_with_data):
    d, m, y = map(str, list_with_data)

    choise = [r for r in input('Что? ').split()]
    if '0' in choise:
        return False
    if checking_correct_data.check_correct_input(category, choise):

        for r in sorted(choise):

            input_info = input(f'{category[int(r) - 1]}: ').replace('\т', '\n')
            dictionary[y][m][d].setdefault(category[int(r) - 1], {})
            # такой подход необходим, чтобы сделать записи с привязкой ко времени
            # (удобство сортировки + хронология + при синхронизации понимеашь что после чего шло)
            now_time = datetime.now()
            data = now_time.strftime('%d/%m/%Y, %H:%M:%S')
            dictionary[y][m][d][category[int(r) - 1]].setdefault(data, input_info)
    else:
        write_desc_in_dict(category, dictionary, list_with_data)


def add_info_in_description(name_and_path, category_description):
    dictionary = values.read_from_json(name_and_path)

    chosen_data = input('дата на добавление:  ').split()
    chosen_data[2] = '20' + chosen_data[2]

    checking_correct_data.create_day_in_dictionary(dictionary, chosen_data)
    values.print_dict_keys_and_values(category_description)
    write_desc_in_dict(category_description, dictionary, chosen_data)

    values.write_in_json(name_and_path, dictionary)


def show_me_data_description(list_with_data, description_path, numberic_mouths_dict, default_mouths_dict):
    print(f'{values.BG_white}показать данные:{values.reset_style}')

    values.print_dict_keys_and_values(values.category, start_enumerate=0)

    dictionary = values.read_from_json(description_path)
    action = input('Что?  ')
    print()
    try:
        match int(action):
            case 1:
                if checking_correct_data.if_day_exist_in_dictionary(dictionary, list_with_data):
                    print_one_day_description(list_with_data, dictionary, numberic_mouths_dict)
                else:
                    print('день еще не заполнен')
            case 2:
                print(
                    '(mm yy, если за месяц; dd mm yy, если за день)\nты можешь написать год без "20", т.е. "23", а не "2023"')
                list_with_data = input('введи дату:  ').split()

                match len(list_with_data):
                    case 2:
                        print_description_stat_moth(list_with_data, dictionary, numberic_mouths_dict,
                                                    default_mouths_dict)
                    case 3:
                        print_one_day_description(list_with_data, dictionary, numberic_mouths_dict)
            case 3:
                print_description_stat_in_range(dictionary, default_mouths_dict, numberic_mouths_dict, a=1)
            case 0:
                raise TypeError
    except TypeError:
        return  False


def print_description_stat_moth(list_with_data, dictionary, numberic_mouths_dict, default_mouths_dict):
    some_month, some_year = list_with_data
    if len(some_year) == 2:
        some_year = '20' + some_year

    if some_year in dictionary.keys():
        if some_month in dictionary[some_year].keys():
            print(f'{default_mouths_dict[int(some_month)].upper()}')
            print()
            days_in_mouth = sorted([int(r) for r in dictionary[some_year][some_month].keys()])
            for some_day in days_in_mouth:
                print_one_day_description(list((some_day, some_month, some_year)), dictionary, numberic_mouths_dict)
                print('\n\n')
                print('=' * 23)

        else:
            print('месяц еще не заполнен')
    else:
        print('год еще не заполнен')
        print('\n\n')


def print_one_day_description(list_with_data, dictionary, numberic_mouths_dict):
    some_day, some_month, some_year = list(map(str, list_with_data))
    if not (some_year.startswith('20')):
        some_year = '20' + some_year

    print(f'\033[47m{some_day}-е {numberic_mouths_dict[int(some_month)]} {some_year}-го\033[0m')

    for action in dictionary[some_year][some_month][some_day].keys():
        print(action.upper())
        today_notes, not_today_notes = sort_info_by_time_add_for_day(
            dictionary[some_year][some_month][some_day][action], list((some_day, some_month, some_year)))

        # сначала выведем то, то было записано в этот день
        for current_date_note in (today_notes, not_today_notes):
            for date_in_note in current_date_note:
                exact_time_writing = date_in_note.split()[1]  # это, чтобы вывести время записи
                if current_date_note == not_today_notes:  # это нужно чтобы выводилась точная дата записи (чтобы показать, дата записи != some_day
                    exact_time_writing = date_in_note
                print(f'\033[4m{exact_time_writing}\033[0m')
                print(f'{dictionary[some_year][some_month][some_day][action][date_in_note]}')
                print()
        print(values.print_line)


def print_description_stat_in_range(dictionary, default_mouths_dict, numberic_mouths_dict, a):
    range_data = input('за какой период?  ').split()
    begin_data, end_data = [int(r) for r in range_data[0].split('.')], [int(r) for r in range_data[1].split('.')]

    all_years_range = [year for year in range(int(begin_data[2]), int(end_data[2]) + 1)]
    existed_years = set(map(str, all_years_range)) & set(dictionary.keys())
    if a == 1:
        for year in existed_years:
            months_in_year = sorted([str(int(r)) for r in dictionary[year].keys()])
            print('=' * 23)
            print(f'{year}-й год, ')

            for month in months_in_year:
                days_in_mouth = sorted([str(int(r)) for r in dictionary[year][month].keys()])
                print('-' * 20)
                print(f'{default_mouths_dict[int(month)].upper()}:')

                for day in days_in_mouth:
                    print_one_day_description(list((day, month, year)), dictionary, numberic_mouths_dict)
                    print()
    elif a == '2':
        for year in existed_years:
            print('=' * 23)
            print(f'{year}-й год, ')
            for month in dictionary[year].keys():
                print('-' * 20)
                print(f'{default_mouths_dict[int(month)]}:')
                for some_day in dictionary[year][month].keys():
                    print(f'\033[4m{some_day}-е {numberic_mouths_dict[int(month)]}\033[0m  ', end='')
                    points = [point for point in dictionary[str(year)][str(month)][str(some_day)].keys()]
                    points = '; '.join(points)
                    print(f'{points}')


def fill_train_diary(dictionary, list_with_data):
    places_to_train = ['Зимний стадион', 'Газпром', 'Фитнес-хаус', 'Елизаровская']
    n_equal_week_day = {1: 'понедельник',
                        2: 'вторник',
                        3: 'среда',
                        4: 'четверг',
                        5: 'пятница',
                        6: 'суббота',
                        7: 'воскресенье'}
    now_data = datetime.now()
    d, m, y = list_with_data
    if data := check_if_not_empty(dictionary, list_with_data):
        print(f'\nСейчас уже есть добавленные данные за {d}.{m}.{y}')
        for key, value in data.items():
            print(f'{key}:  {value}')
    else:
        dictionary[str(y)][str(m)][str(d)].setdefault('день недели', n_equal_week_day[now_data.isoweekday()])

        coach_mark = int(input('оценка тренера?  '))
        dictionary[str(y)][str(m)][str(d)].setdefault('оценка тренера', coach_mark)

        coach_comment = input('что сказал тренер?  ').replace("\т", "\n")
        dictionary[str(y)][str(m)][str(d)].setdefault('что сказал тренер', coach_comment)

        your_mark = int(input('твоя оценка?  '))
        dictionary[str(y)][str(m)][str(d)].setdefault('моя оценка', your_mark)

        your_comment = input('твои ощущения?  ').replace("\т", "\n")
        dictionary[str(y)][str(m)][str(d)].setdefault('мои ощущения', your_comment)

        workout = input('что было?  ').replace("\т", "\n")
        dictionary[str(y)][str(m)][str(d)].setdefault('работа', workout)

        print('где была тренировка?  ')
        values.print_dict_keys_and_values(places_to_train)
        choose_where_was_train = int(input())
        where_was_train = places_to_train[choose_where_was_train]

        dictionary[str(y)][str(m)][str(d)].setdefault('тренировка была в/на', where_was_train)


def check_if_not_empty(dictionary, list_with_data):
    d, m, y = list_with_data
    return dictionary[str(y)][str(m)][str(d)]


def sort_info_by_time_add_for_day(some_part_dict, list_with_data):
    notes_for_this_day = []  # это которые были записаны в этот день
    added_notes = []  # это который были дописаны потом
    day, month, year = list(map(str, list_with_data))
    for datetime_string in some_part_dict:
        if datetime_string.startswith(f'{day}/{month}/{year}'):
            notes_for_this_day.append(datetime_string)
        else:
            added_notes.append(datetime_string)

    notes_for_this_day = sorted(notes_for_this_day,
                                key=lambda some_item: datetime.strptime(some_item, '%d/%m/%Y, %H:%M:%S'))
    added_notes = sorted(added_notes, key=lambda some_item: datetime.strptime(some_item, '%d/%m/%Y, %H:%M:%S'))
    return notes_for_this_day, added_notes
