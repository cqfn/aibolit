from clustering_test import example
from collections import Counter
from typing import List
from collections import OrderedDict


def check_is_common(dict_file, statement_1: int, statement_2: int) -> bool:
    joined_names = Counter(dict_file[statement_1] + dict_file[statement_2])
    duplicates = {element: count for element, count in joined_names.items() if count > 1}.keys()
    return len(list(duplicates)) >= 1

def is_in_range(values: List[int], elem) -> bool:
    return elem >= values[0] and elem <= values[1]

def process_statement(dict_file: OrderedDict, list_statements: List[int], step: int) -> List[List[int]]:
    clusters = []
    for i in list_statements:
        for j in list_statements[:i + step]:
            if i < j and check_is_common(dict_file, i, j):
                if len(clusters) != 0:
                    if not is_in_range(clusters[-1], i):
                        clusters.append([i, j])
                    else:
                        clusters[-1][1] = j
                else:
                    clusters.append([i, j])
    return clusters

def SEMI_beta(dict_file: OrderedDict, mathod_len: int = 24) -> str:
    statements = list(dict_file.keys())
    for step in range(1, mathod_len + 1):
        clusters = process_statement(dict_file, statements, step)
        print(f'\nSTEP: {step}', clusters)

    return 'Done.'

if __name__ == '__main__':
    SEMI_beta(example)
