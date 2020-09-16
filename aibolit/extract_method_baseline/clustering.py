from clustering_test import example  # type: ignore
from collections import Counter
from typing import List
from collections import OrderedDict


def check_is_common(dict_file, statement_1: int, statement_2: int) -> bool:
    joined_names: Counter = Counter(dict_file[statement_1] + dict_file[statement_2])
    duplicates = {element: count for element, count in joined_names.items() if count > 1}.keys()
    return len(list(duplicates)) >= 1


def is_in_range(elem: int, values: List[int]) -> bool:
    return elem >= values[0] and elem <= values[1]


def process_statement(dict_file: OrderedDict, list_statements: List[int], step: int) -> List[List[int]]:
    clusters: List[List[int]] = []
    for stat_1 in list_statements:
        for stat_2 in list_statements[:stat_1 + step]:
            if stat_1 < stat_2 and check_is_common(dict_file, stat_2, stat_2):
                if len(clusters) != 0 and is_in_range(stat_1, clusters[-1]):
                    if not is_in_range(stat_2, clusters[-1]):
                        clusters[-1][1] = stat_2
                else:
                    clusters.append([stat_1, stat_2])
    return clusters


def SEMI_beta(dict_file: OrderedDict, method_len: int) -> str:
    statements = list(dict_file.keys())
    for step in range(1, method_len + 1):
        clusters = process_statement(dict_file, statements, step)
        print(f'\nSTEP: {step}', clusters)
    return 'Done.'


if __name__ == '__main__':
    SEMI_beta(example, 34)
