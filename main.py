import os.path

from work_with_description import write_dict_results, show_me_data_description, fill_train_diary

from work_with_habits import note_habits_results, show_me_data_habit, add_info_in_habits

import time, json
import checking_correct_data


# эта функция нужна, чтобы достать словарик из файла
def read_from_json(name_and_path):
    file = open(name_and_path, 'r', encoding='UTF-8')
    dictionary = json.load(file)
    file.close()
    return dictionary


# эта функция нужна, чтобы занести словарик в файл
def write_in_json(name_and_path, dictionary):
    with open(name_and_path, 'w+', encoding='UTF-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)


# эта функция нужна, чтобы вывести все доступные действия
def print_dict_keys_and_values(tuple):
    for point, action in enumerate(tuple, 1):
        print(f'{point}: {action}')


def mainMenu(list_with_some_data):
    print('-' * 23)
    print('\033[30m\033[41mГЛАВНОЕ МЕНЮ\033[0m')
    functional_desc = ('трекер привычек',
                       'тренировочный дневник',
                       'описание дня',
                       'дополнить данные',
                       'вывести данные на экран',
                       'выйти из программы',
                       )

    print_dict_keys_and_values(functional_desc)

    chose = input('Что выбираем?  ')
    print('-' * 23)

    match chose:
        # вызываем заполнение трекера привычек
        case '1':
            write_habits_day(name_and_path_habits=habit_path,
                             category_habits=category_habits, list_with_some_data=list_with_current_data)

        # вызываем заполнение тренировочного дневника
        case '2':
            write_train_diary_day(name_and_path_diary=train_dairy_path,
                                  list_with_some_data=list_with_current_data)

        # вызываем заполнение итогов дня
        case '3':
            write_description_day(name_and_path_description=description_path,
                                  category_description=category_descripton,
                                  list_with_some_data=list_with_current_data)

        # добавление данных на какой-то определенный день по привычкам\спорт дневнику\итогам дня
        case '4':
            print_dict_keys_and_values(functional_desc[:3])
            choise = input('куда добавим данные?  ')
            match choise:
                case '1':
                    write_habits_day(name_and_path_habits=habit_path,
                                     category_habits=category_habits,
                                     list_with_some_data=write_data_for_adding())
                case '2':
                    write_train_diary_day(name_and_path_diary=train_dairy_path,
                                          list_with_some_data=write_data_for_adding())

                case '3':
                    write_description_day(name_and_path_description=description_path,
                                          category_description=category_descripton,
                                          list_with_some_data=write_data_for_adding())

        # вызываем ouput data (челлендж или итоги дня)
        case '5':
            print('Что показывать? 1 - челлендж-лист, 2 - итоги дня')
            a = input()

            if a == '1':
                show_me_data_habit(list_with_current_data, habit_path, default_mouths_dict, numerated_mouths_dict)

            elif a == '2':
                show_me_data_description(list_with_data=list_with_current_data,
                                         description_path=description_path,
                                         numberic_mouths_dict=numerated_mouths_dict,
                                         default_mouths_dict=default_mouths_dict)

        # а это очень важная фишка на случай, если я захочу вручную закрыть программу, а не просто ее вырубить с локтя
        case '0':
            raise TypeError('ты вышел из меню')

    mainMenu(list_with_some_data)


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
    dictionary = read_from_json(name_and_path_description)

    # если нет текущей даты, то добавляем ее в словарь
    checking_correct_data.create_day_in_dictionary(dictionary, list_with_some_data)

    # показываем все доступные movements для этой категории
    print_dict_keys_and_values(category_description)

    # вызываем функцию для записи данных в словарик
    write_dict_results(category_description, dictionary, list_with_some_data)

    # все это заносим в файл
    write_in_json(name_and_path_description, dictionary)

    # возвращаемся в главное меню
    mainMenu(list_with_some_data)


def write_train_diary_day(name_and_path_diary, list_with_some_data):
    # получаем словарик
    dictionary = read_from_json(name_and_path_diary)

    # если нет текущей даты, то добавляем ее в словарь
    checking_correct_data.create_day_in_dictionary(dictionary, list_with_some_data)

    # вызываем функцию для заполнения данных
    fill_train_diary(dictionary, list_with_some_data)

    # все это заносим в файл
    write_in_json(name_and_path_diary, dictionary)


def write_habits_day(name_and_path_habits, category_habits, list_with_some_data):
    # получаем словарик
    dictionary = read_from_json(name_and_path_habits)

    # если нет текущей даты, то добавляем ее в словарь
    checking_correct_data.create_day_in_dictionary(dictionary, list_with_some_data)

    # показываем все доступные movements для этой категории
    print_dict_keys_and_values(category_habits)

    # вызываем функцию для записи данных в словарик
    note_habits_results(category_habits, dictionary, list_with_some_data)

    # все это заносим в файл
    write_in_json(name_and_path_habits, dictionary)


local_time = time.localtime()
year = str(local_time.tm_year)
month = str(local_time.tm_mon)
today = str(local_time.tm_mday)
list_with_current_data = [today, month, year]

description_path = os.path.abspath(os.path.join('..', 'итоги дня.json'))
habit_path = os.path.abspath(os.path.join('..', 'трекер привычек.json'))
train_dairy_path = os.path.abspath(os.path.join('..', 'спортивный дневник.json'))

category_descripton = ('фактики',
                       'учеба',
                       'треня',
                       'люди',
                       'мысли...',
                       'сон',
                       'отношения'
                       )
category_habits = ('ложиться спать до 22 (+-30мин)',
                   'skillbox',
                   'НЕ кофе',
                   'НЕ игры',
                   'треня',
                   'читать',
                   'писать итоги дня',
                   'ПДД',
                   'не покупать вкусняшки',
                   'говорить с людьми',
                   'держать спину прямо',
                   'выйти в главное меню'
                   )

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
    if not mainMenu(list_with_current_data):
        break
