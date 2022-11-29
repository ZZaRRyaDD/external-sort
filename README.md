# external-sort

**Программа с CLI для сортировки текстовых данных с помощью внешнего многопоточного естественного слияния**

### Установка

**Для запуска проекта вам потребуется установить [poetry](https://python-poetry.org/) и установить зависимости с помощью следующей команды**

```bash
poetry install
```

**После этого запустить виртуальное окружение и запустить программу**

**Использовать программу можно с помощью меню**

```bash
python -m external_sort
```

**Либо при помощи аргументов командной строки**

```bash
python -m external_sort --f test.txt --r True --t 'i'
```

**Предусмотрено**
1. Сортировка данных в форматах csv, txt.
2. Сортировка по невозрастанию/неубыванию
3. Сохранение результата в новый файл (без изменения исходных)
4. Сортировка нескольких файлов одного формата
