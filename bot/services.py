import os.path


def _check_data_file(path: str):
    if not os.path.isfile(path):
        print("Can't read data file with words")
        exit(1)


def _get_words() -> list[str]:
    """
    Converts a txt file with words on separate lines to a list of strings.
    Empty strings would be deleted

    :return: list of str
    """
    path = '../words.txt'
    _check_data_file(path)

    with open(path, 'r', encoding='utf-8') as f:
        file_content = f.read().split('\n')
        words = list(filter(None, file_content))  # remove empty strings

    return words


def get_words_objects() -> list[dict]:
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
