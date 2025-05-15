# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
import shutil
from pathlib import Path
from time import time

from aibolit.config import Config
from aibolit.model.model import PatternRankingModel, scale_dataset, generate_fake_dataset


def test_model_training():
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    config = Config.get_patterns_config()
    model = PatternRankingModel()
    patterns = [x['code'] for x in config['patterns']]
    train_df = generate_fake_dataset()
    model.features_conf = {'features_order': patterns}
    scaled_df = scale_dataset(train_df, model.features_conf, "M4")
    start = time()
    print('Start training...')
    model.fit_regressor(scaled_df[patterns], scaled_df['M4'])
    end = time()
    print(f'End training. Elapsed time: {end - start:.2f} secs')
    # this folder is created by catboost library, impossible to get rid of it
    catboost_folder = Path(cur_file_dir, 'catboost_info')
    if catboost_folder.exists():
        shutil.rmtree(catboost_folder)


def test_train_with_selected_features():
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    model = PatternRankingModel()
    selected_patterns = ['P18', 'P10', 'M2', 'M5']
    train_df = generate_fake_dataset()
    print(f'Features for the whole dataset: {list(train_df.columns)}')
    target = train_df.pop('M4')
    start = time()
    print('Start training...')
    model.fit_regressor(train_df, target, selected_patterns)
    end = time()
    print(f'End training. Elapsed time: {end - start:.2f} secs')
    # this folder is created by catboost library, impossible to get rid of it
    catboost_folder = Path(cur_file_dir, 'catboost_info')
    if catboost_folder.exists():
        shutil.rmtree(catboost_folder)
    print(f'Model features: {list(model.features_conf["features_order"])}')


if __name__ == '__main__':
    test_model_training()
    test_train_with_selected_features()
