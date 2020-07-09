import os
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split

from aibolit.config import Config
import pandas as pd


def preprocess_file(filename: str):
    print('reading dataset from {}'.format(filename))
    df = pd.read_csv(filename)
    df = df[~df["filename"].str.lower().str.contains("test")]
    df = df.dropna().drop_duplicates(subset=df.columns.difference(['filename']))
    df = df[(df.ncss > 20) & (df.ncss < 100) & (df.npath_method_avg < 100000.00)].copy().reset_index()
    return df


def scale(
        df: pd.DataFrame,
        scale_ncss=True,
        **kwargs):

    config = Config.get_patterns_config()
    patterns_codes_set = set([x['code'] for x in config['patterns']])
    metrics_codes_set = [x['code'] for x in config['metrics']]
    exclude_features = set(config['patterns_exclude']).union(set(config['metrics_exclude']))
    target = df[['M4']].values[:, 0].astype(float)

    load_model_file = Path(Config.folder_to_save_model_data(), 'model.pkl')
    print('Test loaded model from file {}:'.format(load_model_file))

    with open(load_model_file, 'rb') as fid:
        model = pickle.load(fid)
        print('Model has been loaded successfully')

    used_codes = set(model.features_conf['features_order'])
    used_codes.add('M4')
    not_scaled_codes = set(patterns_codes_set).union(set(metrics_codes_set)).difference(used_codes).difference(
        exclude_features)
    df.set_index('filename')
    if scale_ncss:
        scaled_df = pd.DataFrame(
            df[used_codes].values / df['M2'].values.reshape((-1, 1)),
            columns=used_codes
        )
        target /= df['M2'].values.astype(float).reshape(-1)
        not_scaled_df = df[not_scaled_codes]
        input = pd.merge(not_scaled_df, scaled_df, left_index=True, right_index=True)
    else:
        input = df

    return input


if __name__ == '__main__':
    current_location: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    dir_to_create = 'target/08'

    train_f = pd.read_csv(Path(current_location, 'target/02/02-train.csv'))
    test_f = pd.read_csv(Path(current_location, 'target/02/02-test.csv'))
    total_elems = train_f.shape[0] + test_f.shape[0]
    print('{} train elems ({}%) and {} test elems test ({}%) of all dataset'.format(
        train_f.shape[0], train_f.shape[0] / total_elems,
        test_f.shape[0], test_f.shape[0] / total_elems))
    # preprocessed_df = preprocess_file(str(Path(current_location, './target/dataset.csv')))
    # train, test = train_test_split(preprocessed_df, test_size=0.3, random_state=42)
    # full_folder_name = Path(current_location, dir_to_create)
    # print('{} post-train elems ({}%) and {} post-test elems test ({}%) of all dataset'.format(
    #     train.shape[0], train.shape[0] / total_elems,
    #     test.shape[0], test.shape[0] / total_elems))
    # if not full_folder_name.exists():
    #     full_folder_name.mkdir()
    # train.to_csv(Path(current_location, dir_to_create, 'train_filtered.csv'))
    # test.to_csv(Path(current_location, dir_to_create, 'train_filtered.csv'))
    df = pd.read_csv(str(Path(current_location, './target/dataset.csv')))
    for i in range(100):
        tr = list(train_f['filename'])
        te = list(test_f['filename'])
        test = df[df['filename'].isin(te)]
        train = df[df['filename'].isin(tr)]
        train.to_csv('temp1.csv')
        test.to_csv('temp2.csv')
        train_pre = preprocess_file('temp1.csv')
        test_pre = preprocess_file('temp2.csv')
        print('{} post-train elems ({}%) and {} post-test elems test ({}%) of all dataset'.format(
            train_pre.shape[0], train_pre.shape[0] / total_elems,
            test_pre.shape[0], test_pre.shape[0] / total_elems))


    # train_scaled = scale(train)
    # test_scaled = scale(test)
    #
    # train_csv_file = Path(current_location, dir_to_create, '08-train.csv')
    # test_csv_file = Path(current_location, dir_to_create, '08-test.csv')
    # if not train_csv_file.parent.exists():
    #     train_csv_file.parent.mkdir(parents=True)
    #
    # train_scaled.to_csv(Path(current_location, dir_to_create, 'train_filtered.csv'))
    # test_scaled.to_csv(Path(current_location, dir_to_create, 'train_filtered.csv'))
