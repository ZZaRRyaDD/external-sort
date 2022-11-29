"""Файл с менюшкой"""
import argparse
import os
from typing import Optional, Union

from external_sort.constants import Actions, Arguments
from external_sort.external_sort import external_multithreaded_natural_merge_sort


def get_file(type_files: str) -> Union[list, bool]:
    """Получение файла и проверка на существование"""
    file_path = input(
        "Введите имя файла(с расширением), откуда нужно считывать данные: ",
    )
    if not os.path.exists(file_path):
        print("Такого файла не существует.")
        return False

    if type_files != '':
        if type_files == file_path[file_path.find('.') + 1:]:
            return [file_path, ]

        print("Расширение файла не то")
        return False
    return [file_path, ]


def get_files(lst_files: list) -> list:
    """Получение файлов для сортировки"""
    choice = input("Введите file, чтобы ввести путь до файла или exit: ")
    type_files = ''
    while choice != "exit":
        if choice == "file":
            result = get_file(type_files)
            if result:
                lst_files.extend(result)
        else:
            print(f"Введите корректное значение. Введено {choice}.")
        choice = input("Введите file, чтобы ввести путь до файла или exit: ")
    return lst_files


def get_output_file(output_file: str) -> str:
    """Получение выводного файла"""
    choice = input(
        "Введите file, чтобы ввести путь до выводного файла или exit: ",
    )
    while choice != "exit":
        if choice == "file":
            output_file = input()
        else:
            print(f"Введите корректное значение. Введено {choice}.")
        choice = input(
            "Введите file, чтобы ввести путь до выводного файла или exit: ",
        )
    return output_file


def get_key(lst_files: list) -> str:
    """Получение ключа, если файл .csv"""
    if lst_files:
        key = ''
        type_file = lst_files[0][lst_files[0].find('.') + 1:]
        if type_file == 'csv':
            key_def = input(
                "Введите ключ(для имени столбца в csv) либо exit: "
            )
            while key_def != "exit":
                if key_def:
                    key = key_def
                else:
                    print("Ключ пустой")
                key_def = input(
                    "Введите ключ(для имени столбца в csv) либо exit: ",
                )

            return key
        print('Для .txt файла(ов) не нужен ключ')
        return ''

    print("Чтобы ввести ключ нужен(ы) файл(ы) для сортировки")
    return ''


def get_reverse(reverse: bool) -> bool:
    """Получение параметра сортировки"""
    value = input("Разворачивать (default False) либо exit: ")
    while value not in ("True", "False", "exit"):
        print(f"Введите корректное значение. Введено {value}.")
        value = input("Разворачивать (default False) либо exit: ")

    if value in ("True", "False"):
        reverse = bool(value)

    return reverse


def get_type_data(type_data: str) -> str:
    """Получение типа данных элементов"""
    type_array = input(
        "Введите тип данных элементов списка(s/i/f) или exit: ",
    )
    while type_array not in ("s", "i", "f", "exit"):
        print(f"Введите корректное значение. Введено: {type_array}.")
        type_array = input(
            "Введите тип данных элементов списка(s/i/f) или exit: "
        )

    if type_array != "exit":
        type_data = type_array

    return type_data


def print_settings(
    lst_files: list,
    key: str,
    output_file: str,
    reverse: bool,
) -> None:
    """Печать настроек сортировки"""
    print("Файлы для сортировки:")
    for i in lst_files:
        print(f"\t{i};")
    if lst_files[0][lst_files[0].find('.') + 1:] == 'csv':
        print(f"Ключ для поиска: {key};")
    if output_file:
        print(f"Выходной файл: {output_file};")
    else:
        print("Выходного файла нет -> файл(ы) сортируется на месте;")
    print(f"Reverse: {reverse};")


def menu() -> None:
    """Печать меню"""
    print(f"{Actions.EXIT} - Выход из программы;")
    print(f"{Actions.ADD_SETTINGS} - Ввод настроек;")
    print(f"{Actions.SORT} - Сортировка.")


def check_fields(
    lst_files: list,
    key: str,
    reverse: bool,
    type_data: str,
) -> bool:
    """Проверка наличия значений у полей"""
    empty_fields = []
    if not lst_files:
        empty_fields.append("Файлы для сортировки")
        if not key:
            empty_fields.append('Ключ, для получения данных')
    else:
        types = []
        not_exist = False
        for i in range(len(lst_files)):
            types.append(lst_files[i][lst_files[i].find('.') + 1:])
            if not os.path.exists(lst_files[i]):
                not_exist = True

        if not_exist:
            empty_fields.append('Не существующие файлы')

        if len(list(set(types))) != 1:
            empty_fields.append('Файлы разных типов данных')
        else:
            if lst_files[0][lst_files[0].find('.') + 1:] == 'csv':
                if not key:
                    empty_fields.append('Ключ, для получения данных')

    if reverse not in (True, False):
        empty_fields.append("Чувствительность к регистру")

    if type_data not in ("s", "i", "f"):
        empty_fields.append("Тип данных")

    if empty_fields:
        print("У вас отсутствуют следующие поля:")
        for field in empty_fields:
            print(f"\t{field}")
        return False

    return True


def start_sort(
    lst_files: list,
    key: str,
    output_file: str,
    reverse: bool,
    type_data: str,
) -> bool:
    """Запуск сортировки"""
    if check_fields(lst_files, key, reverse, type_data):
        external_multithreaded_natural_merge_sort(
            lst_files,
            output_file,
            reverse,
            key,
            type_data,
        )
        return True
    return False


def check_args(args) -> Optional[str]:
    """Обработка cmd аргументов."""
    if not bool(args.f):
        return "not use"

    lst_files = args.f.split(',')
    key = args.k
    output_file = args.o
    reverse = args.r
    type_data = args.t

    start_sort(lst_files, key, output_file, reverse, type_data)


def main() -> None:
    """Точка входа"""
    action = ""
    lst_files = []
    key = ''
    output_file = ''
    reverse = False
    type_data = 's'
    parser = argparse.ArgumentParser(
        description=(
            "Сбор параметров для внешней сортировка естественным слиянием"
        ),
    )
    parser.add_argument(
        Arguments.FILES,
        type=str,
        help="Файлы",
    )
    parser.add_argument(
        Arguments.KEY,
        type=str,
        help="Ключ для csv",
    )
    parser.add_argument(
        Arguments.OUTPUT_FILE,
        type=str,
        help="Выводной файл",
    )
    parser.add_argument(
        Arguments.REVERSE,
        type=bool,
        help="Разворачивать (default False)",
        choices=(True, False),
        default=False,
    )
    parser.add_argument(
        Arguments.TYPE_DATA,
        type=str,
        help="Тип данных (i/s/f)",
        choices=("i", "s", "f"),
        default='s',
    )
    args = parser.parse_args()
    parse = check_args(args)
    while action != Actions.EXIT and parse == "not use":
        menu()
        action = input("Введите желаемое действие: ")
        if action == Actions.ADD_SETTINGS:
            change = ""
            all_field = check_fields(lst_files, key, reverse, type_data)
            if all_field:
                print("Имеющиеся настройки: ")
                print_settings(lst_files, key, output_file, reverse)
                change = input("Желаете изменить параметры?(y/n) ").lower()
                while change not in ("y", "n"):
                    print("Введите корректное значение. ")
                    change = input(
                        "Желаете изменить параметры?(y/n) ",
                    ).lower()

            if all_field is False or change == "y":
                lst_files = get_files(lst_files)
                output_file = get_output_file(output_file)
                key = get_key(lst_files)
                reverse = get_reverse(reverse)
                type_data = get_type_data(type_data)
        elif action == Actions.SORT:
            if not start_sort(
                lst_files,
                key,
                output_file,
                reverse,
                type_data,
            ):
                print("Введены не все параметры")
        elif action == Actions.EXIT:
            print("Сеанс завершен. Успехов!")
        else:
            print(f"Введите корректное значение. Введено {action}.")


if __name__ == '__main__':
    main()
