# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import os
from pathlib import Path

import pandas as pd


def preprocess_file(filename: str):
    print(f'reading dataset from {filename}')
    data = pd.read_csv(filename, index_col=0)
    data = data[~data['filepath'].str.lower().str.contains('test')]
    data = data.dropna().drop_duplicates(
        subset=data.columns.difference(['filepath', 'class_name', 'component_index']))
    data = data[data.M2 < data.M2.quantile(0.99)]
    return data


if __name__ == '__main__':
    target_folder = os.getenv('TARGET_FOLDER')
    if target_folder:
        os.chdir(target_folder)

    current_location: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    dir_to_create = 'target/08'

    train_files = list(pd.read_csv(Path(current_location, 'target/02/02-train.csv'))['filename'])
    test_files = list(pd.read_csv(Path(current_location, 'target/02/02-test.csv'))['filename'])
    train_size = len(train_files)
    test_size = len(test_files)
    total_elems = train_size + test_size
    print(f'{train_size} train elems ({train_size / total_elems}%) and '
          f'{test_size} test elems test ({test_size / total_elems}%) of all dataset')
    df = pd.read_csv(str(Path(current_location, './target/dataset.csv')))
    train = df[df['filepath'].isin(train_files)]
    test = df[df['filepath'].isin(test_files)]
    train.to_csv('train_temp.csv')
    test.to_csv('test_temp.csv')
    train_preprocessed = preprocess_file('train_temp.csv')
    test_preprocessed = preprocess_file('test_temp.csv')
    total_size = train_preprocessed.shape[0] + test_preprocessed.shape[0]
    print(f'{train_preprocessed.shape[0]} train elems '
          f'({train_preprocessed.shape[0] / total_size}%) and '
          f'{test_preprocessed.shape[0]} test elems '
          f'({test_preprocessed.shape[0] / total_size}%) of processed dataset')
    Path('train_temp.csv').unlink()
    Path('test_temp.csv').unlink()
    path_to_create = Path(dir_to_create)
    if not path_to_create.exists():
        path_to_create.mkdir(parents=True)
    train_csv_path = Path(path_to_create, '08-train.csv')
    test_csv_path = Path(path_to_create, '08-test.csv')
    train_preprocessed.to_csv(train_csv_path, encoding='utf-8')
    test_preprocessed.to_csv(test_csv_path, encoding='utf-8')
