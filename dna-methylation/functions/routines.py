import re


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def split_words(text):
    rgx = re.compile(r"((?:(?<!'|\w)(?:\w-?'?)+(?<!-))|(?:(?<='|\w)(?:\w-?'?)+(?=')))")
    return rgx.findall(text)


def only_words(words):
    passed_words = []
    for word in words:
        if not is_float(word):
            passed_words.append(word)
    return passed_words


def get_na_values():
    na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>',
                 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', '-', '--']
    return na_values


def label_race(row, candidate, column):
    target_string = row[column]
    if isinstance(target_string, str):
        if candidate in target_string:
            return 'yes'
        else:
            return 'no'
    else:
        return 'no'