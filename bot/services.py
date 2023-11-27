import os.path
import random

from peewee import fn

from models import Word


def _check_data_file(path: str) -> None:
    """
    Проверяет, существует ли файл с названиями. Если нет - завершает программу с кодом 1

    :param path: путь к файлу
    :return: None
    """
    if not os.path.isfile(path):
        print("Can't read data file with words")
        exit(1)


def _get_words() -> list[str]:
    """
    Преобразует текстовый файл со словами в отдельных строках в список строк.
    Пустая строка будет удалена

    :return: лист слов из файла
    """
    path = '../words.txt'
    _check_data_file(path)

    with open(path, 'r', encoding='utf-8') as f:
        file_content = f.read().split('\n')
        words = list(filter(None, file_content))  # удалит пустые строки

    return words


def get_words_objects() -> list[dict]:
    """
    Преобразует список слов в модель для бд

    :return: лист словарей в соответствии с моделью Word
    """
    word_list = _get_words()
    words = []

    for index, _word in enumerate(word_list, start=1):
        words.append({
            'id': index,
            'word': _word,
            'show_num': 0,
            'vote_num': 0
        })

    return words


def get_words_ids() -> tuple[int, int]:
    """
    Возвращает два случайных ида названий из бд

    :return: кортеж с парой идов
    """
    max_id = Word.select(fn.MAX(Word.id)).scalar()  # получает значение максимального ида
    id_1 = id_2 = random.randint(1, max_id)

    while id_1 == id_2:
        id_2 = random.randint(1, max_id)

    return id_1, id_2
