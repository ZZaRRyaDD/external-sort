"""Модуль реализации внешней многопоточной сортировкой слияния"""
import multiprocessing
import os
import pathlib
from typing import Optional, Union

from external_sort.my_file import MyFile

PathTypeList = Union[list, pathlib.Path]
PathTypeStr = Union[MyFile, pathlib.Path]


def valid_item(item: str, type_data: str) -> bool:
    """Функция проверки считанного значения"""
    value = None
    if type_data == 'i':
        value = (
            item.replace('-', '').replace('.', '').replace('\n', '').isdigit()
        )
    elif type_data == 's':
        value = False if item in ("", "'\n", "\'", "\'\n") else True
    elif type_data == 'f':
        value = (
            item.replace('-', '').replace('.', '').replace('\n', '').isdigit()
        )
    return value


def compare(first: str, second: str, type_data: str) -> int:
    """Функция сравнения"""
    value = 0
    if type_data == 'i':
        if int(first) < int(second):
            value = -1
        elif int(first) > int(second):
            value = 1
        else:
            value = 0
    elif type_data == 's':
        if str(first) < str(second):
            value = -1
        elif str(first) > str(second):
            value = 1
        else:
            value = 0
    elif type_data == 'f':
        if float(first) < float(second):
            value = -1
        elif float(first) > float(second):
            value = 1
        else:
            value = 0

    return value


def check_sorting(main_file: MyFile, reverse: bool) -> bool:
    """Функция проверки отсортированности файла"""
    sort = True
    main_file.open_file('r')
    count_str1, count_str2 = 0, 0
    str1, str2 = '', ''
    while not valid_item(str(str1), main_file.type_data):
        str1 = main_file.read_file()
    count_str1 += 1

    while not valid_item(str(str2), main_file.type_data):
        str2 = main_file.read_file()

    while (count_str1 + count_str2) < main_file.count_lines:
        if (
            compare(str1, str2, main_file.type_data) not in
            ((1 if reverse else -1), 0)
        ):
            sort = False
            break

        count_str2 += 1
        str1 = str2
        str2 = main_file.read_file()
        while not valid_item(str(str2), main_file.type_data):
            str2 = main_file.read_file()
            if (count_str1 + count_str2) == main_file.count_lines:
                break
    main_file.close_file()
    return sort


def split_file(
    main_file: MyFile,
    first_file: MyFile,
    second_file: MyFile,
    reverse: bool,
) -> None:
    """Функция разделения файлов"""
    main_file.open_file('r')
    first_file.clean_file()
    first_file.open_file('a')
    second_file.clean_file()
    second_file.open_file('a')
    count_str1, count_str2 = 0, 0
    mark = 1
    str1, str2 = '', ''
    while not valid_item(str(str1), main_file.type_data):
        str1 = main_file.read_file()
    count_str1 += 1

    if (count_str1 + count_str2) < main_file.count_lines:
        str1 = str1 + "\n" if "\n" not in str1 else str1
        first_file.write_file(str1)
        first_file.count_lines += 1

    if (count_str1 + count_str2) < main_file.count_lines:
        while not valid_item(str(str2), main_file.type_data):
            str2 = main_file.read_file()

    while (count_str1 + count_str2) < main_file.count_lines:
        str2 = str2 + "\n" if "\n" not in str2 else str2
        if (
            compare(str1, str2, main_file.type_data) in
            ((1 if reverse else -1), 0)
        ):
            if mark == 1:
                first_file.write_file(str2)
                first_file.count_lines += 1
                mark = 1
                count_str1 += 1
            else:
                second_file.write_file(str2)
                second_file.count_lines += 1
                mark = 2
                count_str2 += 1
        else:
            if mark == 1:
                count_str2 += 1
                first_file.write_file("'\n")
                second_file.write_file(str2)
                second_file.count_lines += 1
                mark = 2
            else:
                count_str1 += 1
                second_file.write_file("'\n")
                first_file.write_file(str2)
                first_file.count_lines += 1
                mark = 1

        str1 = str2
        str2 = main_file.read_file()
        while not valid_item(str(str2), main_file.type_data):
            str2 = main_file.read_file()
            if (count_str1 + count_str2) == main_file.count_lines:
                break

    if mark == 1:
        first_file.write_file("'\n")
    else:
        second_file.write_file("'\n")

    first_file.close_file()
    second_file.close_file()


def end_block(file: MyFile):
    """Функция проверки конца блока"""
    item = file.read_file()
    res = True if item in ("", "'\n", "\'", "\'\n") else False
    return res, item


def merge(
    main_file: MyFile,
    first_file: MyFile,
    second_file: MyFile,
    reverse: bool,
) -> None:
    """Слияние файлов"""
    count_str1, count_str2 = 0, 0
    end_first_file, end_second_file = (
        first_file.count_lines == 0,
        second_file.count_lines == 0,
    )
    str1, str2 = '', ''
    main_file.open_file('a')
    first_file.open_file('r')
    second_file.open_file('r')

    if count_str1 < first_file.count_lines:
        str1 = first_file.read_file()

    if count_str2 < second_file.count_lines:
        str2 = second_file.read_file()

    while (
        (count_str1 + count_str2) <
        (first_file.count_lines + second_file.count_lines)
    ):
        end_first_section, end_second_section = False, False
        end_first_section = (
            end_first_file
            if end_first_file
            else end_first_section
        )
        end_second_section = (
            end_second_file
            if end_second_file
            else end_second_section
        )
        while not end_first_section and not end_second_section:
            if (
                compare(str1, str2, main_file.type_data) in
                ((1 if reverse else -1), 0)
            ):
                main_file.write_file(str1)
                main_file.count_lines += 1
                end_first_section, str1 = end_block(first_file)
                count_str1 += 1
                while not valid_item(str(str1), main_file.type_data):
                    str1 = first_file.read_file()
                    if count_str1 == first_file.count_lines:
                        end_first_file = True
                        break
                str1 = str1 + "\n" if "\n" not in str1 else str1
            else:
                main_file.write_file(str2)
                main_file.count_lines += 1
                end_second_section, str2 = end_block(second_file)
                count_str2 += 1
                while not valid_item(str(str2), main_file.type_data):
                    str2 = second_file.read_file()
                    if count_str2 == second_file.count_lines:
                        end_second_file = True
                        break
                str2 = str2 + "\n" if "\n" not in str2 else str2

        while not end_first_section:
            main_file.write_file(str1)
            main_file.count_lines += 1
            end_first_section, str1 = end_block(first_file)
            count_str1 += 1
            while not valid_item(str(str1), main_file.type_data):
                str1 = first_file.read_file()
                if count_str1 == first_file.count_lines:
                    end_first_section = True
                    break
            str1 = str1 + "\n" if "\n" not in str1 else str1

        while not end_second_section:
            main_file.write_file(str2)
            main_file.count_lines += 1
            end_second_section, str2 = end_block(second_file)
            count_str2 += 1
            while not valid_item(str(str2), main_file.type_data):
                str2 = second_file.read_file()
                if count_str2 == second_file.count_lines:
                    end_second_file = True
                    break
            str2 = str2 + "\n" if "\n" not in str2 else str2

    end_first_section, end_second_section = False, False
    while not end_first_section and count_str1 < first_file.count_lines:
        main_file.write_file(str1)
        main_file.count_lines += 1
        end_first_section, str1 = end_block(first_file)
        count_str1 += 1
        while not valid_item(str(str1), main_file.type_data):
            str1 = first_file.read_file()
            if count_str1 == first_file.count_lines:
                end_first_section = True
                break
        str1 = str1 + "\n" if "\n" not in str1 else str1

    while not end_second_section and count_str2 < second_file.count_lines:
        main_file.write_file(str2)
        main_file.count_lines += 1
        end_second_section, str2 = end_block(second_file)
        count_str2 += 1
        while not valid_item(str(str2), main_file.type_data):
            str2 = second_file.read_file()
            if count_str2 == second_file.count_lines:
                end_second_file = True
                break
        str2 = str2 + "\n" if "\n" not in str2 else str2

    first_file.close_file()
    second_file.close_file()


def enter_point(
    main_file: MyFile,
    first_file: MyFile,
    second_file: MyFile,
    reverse: bool,
) -> None:
    """Точка входа в программу"""
    print(f"{multiprocessing.current_process().name} начал")
    if main_file.count_lines > 1:
        while not check_sorting(main_file, reverse):
            split_file(main_file, first_file, second_file, reverse)
            main_file.clean_file()
            merge(main_file, first_file, second_file, reverse)
            main_file.close_file()
    first_file.remove()
    second_file.remove()
    print(f"{multiprocessing.current_process().name} закончил")


def copy_in_file(main_file: MyFile, first_file: MyFile, last_item: str):
    """Функция копирования информации в выходной файл"""
    first_file.open_file('r')
    count_str = 0

    while count_str < first_file.count_lines:
        str1 = first_file.read_file()
        while not valid_item(str(str1), main_file.type_data):
            str1 = first_file.read_file()
        str1 = (
            '\n' + str1
            if last_item != '' and last_item[-1:] != '\n'
            else str1
        )
        main_file.write_file(str1)
        last_item = str1
        main_file.count_lines += 1
        count_str += 1
    first_file.close_file()
    return main_file, last_item


def write_to_output(
    src: PathTypeList,
    output: MyFile,
    key: str,
    type_data: str,
) -> PathTypeStr:
    """Начало записи в выходной файл"""
    output.clean_file()
    output.open_file('a')
    last_item = ''
    for file in src:
        output, last_item = copy_in_file(
            output,
            MyFile(file, key, type_data),
            last_item,
        )
    output.close_file()
    return output


def external_multithreaded_natural_merge_sort(
    src: PathTypeList,
    output: Optional[str] = '',
    reverse: bool = False,
    key: str = '',
    type_data: str = 's',
) -> None:
    """Запуск сортировки"""
    if output:
        if os.path.exists(output):
            src = write_to_output(
                src,
                MyFile(output, key, type_data),
                key,
                type_data,
            )

    if isinstance(src, MyFile):
        lst_split_files = [
            MyFile("file0.txt", key, type_data),
            MyFile("file1.txt", key, type_data),
        ]
        enter_point(src, lst_split_files[0], lst_split_files[1], reverse)
    elif isinstance(src, list):
        processes = []
        lst_split_files = [
            (
                MyFile(f"file{i}.txt", key, type_data),
                MyFile(f"file{i + 1}.txt", key, type_data),
            )
            for i in range(0, 2 * len(src), 2)
        ]
        for index, file in enumerate(src):
            args = (
                MyFile(file, key, type_data),
                lst_split_files[index][0],
                lst_split_files[index][1],
                reverse,
            )
            proc = multiprocessing.Process(target=enter_point, args=args)
            proc.start()
            proc.join()
            processes.append(proc)
