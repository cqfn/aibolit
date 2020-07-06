import os
import pickle
from pathlib import Path

from aibolit.config import Config
import pandas as pd


def preprocess_file(
        filename,
        scale_ncss=True,
        **kwargs):
    print('reading dataset from {}'.format(Config.dataset_file()))
    df = pd.read_csv(filename).set_index('filename')
    df = df[~df["filename"].str.lower().str.contains("test")]
    config = Config.get_patterns_config()
    if self.do_rename_columns:
        p_codes = \
            [x['code'] for x in config['patterns']] \
            + ['lines' + x['code'] for x in config['patterns']]
        m_codes = [x['code'] for x in config['metrics']]
        keys = p_codes + m_codes
        vals = \
            [x['name'] for x in config['patterns']] \
            + ['lines' + x['name'] for x in config['patterns']] \
            + [x['name'] for x in config['metrics']]

        replace_dict = dict(zip(keys, vals))
        df = df.rename(replace_dict)
        df.columns = vals
        print('Columns renamed:' + df.head())

    df = df.dropna().drop_duplicates(subset=df.columns.difference(['filename']))
    df = df[(df.ncss > 20) & (df.ncss < 100) & (df.npath_method_avg < 100000.00)].copy().reset_index()
    patterns_codes_set = set([x['code'] for x in config['patterns']])
    metrics_codes_set = [x['code'] for x in config['metrics']]
    target = df[['M4']].values[:, 0]

    load_model_file = Path(Config.folder_to_save_model_data(), 'model.pkl')
    print('Test loaded model from file {}:'.format(load_model_file))

    with open(load_model_file, 'rb') as fid:
        model = pickle.load(fid)
        print('Model has been loaded successfully')

    used_codes = set(model.features_conf)
    used_codes.add('M4')
    not_scaled_codes = set(patterns_codes_set).union(set(metrics_codes_set)).difference(used_codes)
    if scale_ncss:
        scaled_df = pd.DataFrame(
            df[used_codes].values / df['M2'].values.reshape((-1, 1)),
            columns=used_codes
        )
        target /= df['M2'].values.reshape(-1)
        not_scaled_df = df[not_scaled_codes]
        input = pd.merge(not_scaled_df, scaled_df, left_index=True, right_index=True)
    else:
        input = df

    return input

if __name__ == '__main__':
    input = preprocess_file('./target/dataset.csv')
    parent_cwd = Path(os.getcwd()).parent
    train_csv_path = Path(parent_cwd, 'target/02/02-train.csv')
    train_csv_path = Path(parent_cwd, 'target/02/02-test.csv')
    path
    path_csv_out = str(Path(, SPLIT_CSV, 'target/02/02-train.csv'))
    df = pd.read_csv(path_csv_out)
    train, test = train_test_split(df['filename'], test_size=0.3, random_state=42)
    train_csv_file = str(Path(current_location, DIR_TO_CREATE, '02-train.csv'))
    test_csv_file = str(Path(current_location, DIR_TO_CREATE, '02-test.csv'))

    train_rows = input[input['filename'] in ]
