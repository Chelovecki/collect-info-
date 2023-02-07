import os.path, values

from work_with_description import write_desc_in_dict, show_me_data_description, fill_train_diary

from work_with_habits import note_habits_results, show_me_data_habit, add_info_in_habits

import time, checking_correct_data




def main_menu(list_with_some_data):
    print(values.print_line)
    print(f'{values.BG_red}ГЛАВНОЕ МЕНЮ{values.reset_style}')
    # этот пункт я не стал засовывать в values.py, потому что он относится к программным.
    # а не к тому, что можно (и следует) менять/добавлять пользователю
    functional_desc = ('выйти из программы',
                       'трекер привычек',
                       'тренировочный дневник',
                       'описание дня',
                       'дополнить данные',
                       'вывести данные на экран',
                       )

    values.print_dict_keys_and_values(functional_desc, start_enumerate=0)

    chose = input('Что выбираем?  ')
    print(values.print_line)

    match chose:
        # вызываем заполнение трекера привычек
        case '1':
            write_habits_day(habit_path, values.category_habits, list_with_current_data)

        # вызываем заполнение тренировочного дневника
        case '2':
            write_train_diary_day(train_dairy_path, list_with_current_data)

        # вызываем заполнение итогов дня
        case '3':
            write_description_day(description_path, values.category_descripton, list_with_current_data)

        # добавление данных на какой-то определенный день по привычкам\спорт дневнику\итогам дня
        case '4':
            values.print_dict_keys_and_values(functional_desc[:3])
            choise = input('куда добавим данные?  ')
            match choise:
                case '1':
                    write_habits_day(habit_path, values.category_habits, write_data_for_adding())
                case '2':
                    write_train_diary_day(train_dairy_path, write_data_for_adding())

                case '3':
                    write_description_day(description_path, values.category_descripton, write_data_for_adding())

        # вызываем output data (челлендж или итоги дня)
        case '5':
            print('Что показывать? 1 - челлендж-лист, 2 - итоги дня (0, чтобы вернуться)')
            a = input()

            if a == '1':
                show_me_data_habit(list_with_current_data, habit_path, default_mouths_dict, numerated_mouths_dict)

            elif a == '2':
                show_me_data_description(list_with_current_data, description_path, numerated_mouths_dict, default_mouths_dict)

        # а это очень важная фишка на случай, если я захочу вручную закрыть программу, а не просто ее вырубить с локтя
        case '0':
            exit()

    main_menu(list_with_some_data)


def write_data_for_adding():
    data_to_add = input('введи дату на добавление dd mm yy:  ').split()
    if (input('ты точно уверен в корректности ввода даты?(enter - yes, anything else - no)  ')) == '':
        if len(data_to_add[2]) != 4:
            data_to_add[2] = '20' + data_to_add[2]
        data_to_add = list(map(int, data_to_add))
        return data_to_add
    else:
        write_data_for_adding()


def write_description_day(name_and_path_description, category_description, list_with_some_data):
    # получаем словарик
    dictionary = values.read_from_json(name_and_path_description)

    # если нет текущей даты, то добавляем ее в словарь
    checking_correct_data.create_day_in_dictionary(dictionary, list_with_some_data)

    # показываем все доступные movements для этой категории
    values.print_dict_keys_and_values(category_description, start_enumerate=0)

    # вызываем функцию для записи данных в словарик
    write_desc_in_dict(category_description, dictionary, list_with_some_data)

    # все это заносим в файл
    values.write_in_json(name_and_path_description, dictionary)

    # возвращаемся в главное меню
    main_menu(list_with_some_data)


def write_train_diary_day(name_and_path_diary, list_with_some_data):
    # получаем словарик
    dictionary = values.read_from_json(name_and_path_diary)

    # если нет текущей даты, то добавляем ее в словарь
    checking_correct_data.create_day_in_dictionary(dictionary, list_with_some_data)

    # вызываем функцию для заполнения данных
    fill_train_diary(dictionary, list_with_some_data)

    # все это заносим в файл
    values.write_in_json(name_and_path_diary, dictionary)


def write_habits_day(name_and_path_habits, category_habits, list_with_some_data):
    # получаем словарик
    dictionary = values.read_from_json(name_and_path_habits)

    # если нет текущей даты, то добавляем ее в словарь
    checking_correct_data.create_day_in_dictionary(dictionary, list_with_some_data)

    # показываем все доступные movements для этой категории
    values.print_dict_keys_and_values(values.category_habits, start_enumerate=0)

    # вызываем функцию для записи данных в словарик
    note_habits_results(values.category_habits, dictionary, list_with_some_data)

    # все это заносим в файл
    values.write_in_json(name_and_path_habits, dictionary)


local_time = time.localtime()
year = str(local_time.tm_year)
month = str(local_time.tm_mon)
today = str(local_time.tm_mday)
list_with_current_data = [today, month, year]

description_path = os.path.abspath(os.path.join('jsons\итоги дня.json'))
habit_path = os.path.abspath(os.path.join('jsons\трекер привычек.json'))
train_dairy_path = os.path.abspath(os.path.join('jsons\спортивный дневник.json'))




numerated_mouths_dict = {1: 'января',
                         2: 'февраля',
                         3: 'марта',
                         4: 'апреля',
                         5: 'мая',
                         6: 'июня',
                         7: 'июля',
                         8: 'августа',
                         9: 'сентября',
                         10: 'октября',
                         11: 'ноября',
                         12: 'декабря',
                         }
default_mouths_dict = {1: 'январь',
                       2: 'февраль',
                       3: 'март',
                       4: 'апрель',
                       5: 'май',
                       6: 'июнь',
                       7: 'июль',
                       8: 'август',
                       9: 'сентябрь',
                       10: 'октябрь',
                       11: 'ноябрь',
                       12: 'декабрь',
                       }

print(
    'привет, ты попал в мою программу для ведения привычек, '
    'для записи итогов дня, для ведения тренировочного дневника\n'
    'чтобы дописать информацию за какой-то промежуток времени, '
    'тебе надо ввести номер того, что ты хочешь дописать. '
    'то есть, если хочешь написать итоги дня за вчера, '
    'тебе надо написать "33"')
while True:
    if not main_menu(list_with_current_data):
        break
