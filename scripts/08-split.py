import os
from pathlib import Path

import pandas as pd


def preprocess_file(filename: str):
    print('reading dataset from {}'.format(filename))
    df = pd.read_csv(filename, index_col=0)
    df = df[~df["filepath"].str.lower().str.contains("test")]
    df = df.dropna().drop_duplicates(subset=df.columns.difference(["filepath", "class_name", "component_index"]))
    df = df[(df.M2 > 20) & (df.M2 < 100)].copy()
    return df


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
    print('{} train elems ({}%) and {} test elems test ({}%) of all dataset'.format(
        train_size, train_size / total_elems,
        test_size, test_size / total_elems))
    df = pd.read_csv(str(Path(current_location, './target/dataset.csv')))
    train = df[df['filepath'].isin(train_files)]
    test = df[df['filepath'].isin(test_files)]
    train.to_csv('train_temp.csv')
    test.to_csv('test_temp.csv')
    train_preprocessed = preprocess_file('train_temp.csv')
    test_preprocessed = preprocess_file('test_temp.csv')
    total_size = (train_preprocessed.shape[0] + test_preprocessed.shape[0])
    print('{} train elems ({}%) and {} test elems test ({}%) of processed dataset'.format(
        train_preprocessed.shape[0], train_preprocessed.shape[0] / total_size,
        test_preprocessed.shape[0], test_preprocessed.shape[0] / total_size))
    Path('train_temp.csv').unlink()
    Path('test_temp.csv').unlink()
    path_to_create = Path(dir_to_create)
    if not path_to_create.exists():
        path_to_create.mkdir(parents=True)
    train_csv_path = Path(path_to_create, '08-train.csv')
    test_csv_path = Path(path_to_create, '08-test.csv')
    train_preprocessed.to_csv(train_csv_path, encoding='utf-8')
    test_preprocessed.to_csv(test_csv_path, encoding='utf-8')
