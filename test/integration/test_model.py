# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
    scaled_df = scale_dataset(train_df, model.features_conf)
    start = time()
    print('Start training...')
    model.fit_regressor(scaled_df[patterns], scaled_df['M4'])
    end = time()
    print('End training. Elapsed time: {:.2f} secs'.format(end - start))
    # this folder is created by catboost library, impossible to get rid of it
    catboost_folder = Path(cur_file_dir, 'catboost_info')
    if catboost_folder.exists():
        shutil.rmtree(catboost_folder)


if __name__ == '__main__':
    test_model_training()
