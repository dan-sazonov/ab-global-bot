def _file_to_list(path: str) -> list[str]:
    """
    Converts a txt file with words on separate lines to a list of strings.
    Empty strings would be deleted

    :param path: absolute or relative path to the txt file
    :return: list of str
    """
    with open(path, 'r', encoding='utf-8') as f:
        file_content = f.read().split('\n')
        words = list(filter(None, file_content))  # remove empty strings

    return words