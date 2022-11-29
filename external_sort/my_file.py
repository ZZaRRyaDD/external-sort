"""Реализация класса MyFile"""
import csv
import os
from typing import Union


class MyFile:
    """Класс для работы с txt и csv файлами"""

    def __init__(self, path: str, key: str, type_data: str) -> None:
        self.__path = path
        self.check_exist()
        self.__ptr = None
        self.__reader = None
        self.__writer = None
        self.__type_data = type_data
        self.__type = path[path.find('.') + 1:]
        self.__lines = 0
        self.__key = '' if self.__type != 'csv' else key
        self.calculate_count_lines()

    @property
    def count_lines(self) -> int:
        """Getter для количества строк"""
        return self.__lines

    @count_lines.setter
    def count_lines(self, count: int):
        """Setter для количества строк"""
        self.__lines = count

    @property
    def type_data(self):
        """Getter для типа данных файла"""
        return self.__type_data

    def create_file(self):
        """Метод для создания файла"""
        if not os.path.exists(self.__path):
            with open(self.__path, "x", encoding='utf-8') as _:
                pass
        else:
            self.clean_file()

    def check_exist(self):
        """Метод для проверки существования файла"""
        if not os.path.exists(self.__path):
            self.create_file()

    def calculate_count_lines(self):
        """Метод для вычисления количества строк"""
        if self.__ptr is None:
            self.open_file('r')

        if self.__type == 'txt':
            for _ in self.__ptr:
                self.__lines += 1
        elif self.__type == 'csv':
            for _ in self.__reader:
                self.__lines += 1

        self.close_file()

    def open_file(self, mode: str = 'r'):
        """Метод для открытия файла"""
        if self.__ptr is not None:
            self.close_file()

        if self.__type == 'txt':
            self.__ptr = open(self.__path, mode, encoding='utf-8')
        elif self.__type == 'csv':
            if mode == 'r':
                self.__ptr = open(self.__path, mode, encoding='utf-8')
                self.__reader = csv.DictReader(self.__ptr)
            elif mode == 'a':
                self.__ptr = open(
                    self.__path,
                    mode,
                    newline='',
                    encoding='utf-8',
                )
                self.__writer = csv.DictWriter(
                    self.__ptr,
                    fieldnames=[self.__key],
                )
                self.__writer.writeheader()
            elif mode == 'w':
                self.__ptr = open(
                    self.__path,
                    mode,
                    newline='',
                    encoding='utf-8',
                )
                self.__writer = csv.DictWriter(
                    self.__ptr,
                    fieldnames=[self.__key],
                )

    def close_file(self) -> None:
        """Метод для закрытия файла"""
        if self.__ptr is not None:
            self.__ptr.close()
            self.__ptr = None
            self.__reader = None
            self.__writer = None

    def read_file(self) -> str:
        """Метод для чтения файла"""
        if self.__ptr is None:
            self.open_file('r')

        if self.__type == 'txt':
            try:
                return self.__ptr.readline()
            except StopIteration:
                return ''

        if self.__type == 'csv':
            try:
                return next(self.__reader)[self.__key]
            except StopIteration:
                return ''

    def transform_item(self, item: str) -> Union[str, int, float]:
        """Метод для преобразования элемента при записи в csv файл"""
        if self.__type_data == 'i':
            item = int(item)
        elif self.__type_data == 's':
            item = str(item).replace('\n', '')
        elif self.__type_data == 'f':
            item = float(item)

        return item

    def write_file(self, item: str) -> None:
        """Метод для записи в файл"""
        if self.__type == 'txt':
            self.__ptr.write(str(item))
        elif self.__type == 'csv':
            if item:
                self.__writer.writerow(
                    {self.__key: self.transform_item(item)},
                )

    def clean_file(self) -> None:
        """Метод для очистки файла"""
        self.open_file('w')
        self.write_file('')
        self.close_file()
        self.count_lines = 0

    def remove(self):
        """Метод для удаления файла"""
        self.close_file()
        os.remove(self.__path)
        self.__path = None
