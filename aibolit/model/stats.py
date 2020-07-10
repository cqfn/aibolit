import pickle
import tarfile
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
from aibolit.config import Config
from aibolit.model.model import TwoFoldRankingModel  # noqa: F401 type: ignore


class Stats(object):

    def aibolit_stat(self):
        dataset_archive = Config.get_dataset_archive()
        try:
            tar = tarfile.open(str(dataset_archive))
            tar.extractall(path=dataset_archive.parent)
            tar.close()
            print('Dataset has been unzipped successfully')
        except Exception as e:
            print('Dataset unzip failed: {}'.format(str(e)))
            return 1

        test_csv = pd.read_csv(Path(dataset_archive.parent, '08-test.csv'))
        load_model_file = Config.folder_model_data()
        print('Loading model from file {}:'.format(load_model_file))
        with open(load_model_file, 'rb') as fid:
            model = pickle.load(fid)
            print('Model has been loaded successfully')
        scaled_dataset = model.scale_dataset(test_csv)
        cleaned_dataset = scaled_dataset[model.features_conf['features_order'] + ['M2']]
        ranked, _, acts_complexity, acts = self.check_impact(
            cleaned_dataset.values,
            model
        )

        m, p = self.count_acts(acts, ranked)
        return self.get_table(model.features_conf['features_order'], m, p, acts_complexity)

    def count_acts(self, acts, ranked):
        patterns_numbers = ranked[:, 0]
        # number of times when pattern was on first place,
        # if we decrease pattern by 1/ncss
        m = np.zeros(ranked.shape[1])
        # number of times when pattern was on first place,
        # if we increase pattern by 1/ncss
        p = np.zeros(ranked.shape[1])
        for i in range(len(patterns_numbers)):
            if acts[i] == 1:
                m[patterns_numbers[i]] += 1
            elif acts[i] == 2:
                p[patterns_numbers[i]] += 1
        return m, p

    def get_patterns_name(self):
        only_patterns = []
        patterns_code = []
        config = Config.get_patterns_config()
        for x in config['patterns']:
            if x['code'] not in config['patterns_exclude']:
                only_patterns.append(x['name'])
                patterns_code.append(x['code'])
        features_number = len(only_patterns)
        print("Number of features: ", features_number)
        patterns = {x['code']: x['name'] for x in config['patterns']}
        metrics = {x['code']: x['name'] for x in config['metrics']}
        replace_dict = dict(patterns, **metrics)
        return replace_dict

    def get_table(
            self,
            features_conf: Dict[Any, Any],
            m,
            p,
            acts_complexity) -> pd.DataFrame:
        """
        Prints results, given with `check_impact`.


        :param features_conf: features config of model
        :param m: number of times when pattern was on first place,
        if we decrease pattern by 1/ncss
        :param p: number of times when pattern was on first place,
        if we increase pattern by 1/ncss
        :param acts_complexity:

        """

        df = pd.DataFrame(columns=[
            'pattern', ' -1(top1)', '+1(top1)',
            'p-c-', 'p+c+', 'p-c+', 'p+c-', 'p-c=',
            'p+c='])
        replace_dict = self.get_patterns_name()
        for i in range(len(features_conf)):
            top_minus = int(m[i])
            top_plus = int(p[i])
            p_minus_c_minus = int(acts_complexity[i, 0])
            p_plus_c_plus = int(acts_complexity[i, 4])
            p_minus_c_plus = int(acts_complexity[i, 1])
            p_plus_c_minus = int(acts_complexity[i, 3])
            p_minus_c_euq = int(acts_complexity[i, 2])
            p_plus_c_euq = int(acts_complexity[i, 5])
            pattern = replace_dict.get(features_conf[i])
            df = df.append({
                'pattern': pattern, ' -1(top1)': top_minus, '+1(top1)': top_plus,
                'p-c-': p_minus_c_minus, 'p+c+': p_plus_c_plus, 'p-c+': p_minus_c_plus,
                'p+c-': p_plus_c_minus, 'p-c=': p_minus_c_euq,
                'p+c=': p_plus_c_euq
            }, ignore_index=True)

        return df

    def divide_array(self, X, pattern_idx):
        """ Divide dataset.

        :param X: dataset
        :param pattern_idx: pattern index
        :return:
        1st is dataset with pattern where pattern can be null,
        2nd is dataset with pattern where pattern is not null,
        """
        nulls = []
        not_nulls = []
        for snipp in X:
            if snipp[pattern_idx] == 0:
                nulls.append(snipp)
            else:
                not_nulls.append(snipp)

        return np.array(nulls), np.array(not_nulls)

    def get_minimum(self, c1, c2, c3):
        """
        Args:
            c1, c2, c3: np.array with shape (number of snippets, ).
        Returns:
            c: np.array with shape (number of snippets, ) -
            elemental minimum of 3 arrays.
            number: np.array with shape (number of snippets, ) of
            arrays' numbers with minimum elements.            .
        """

        c = np.vstack((c1, c2, c3))

        return np.min(c, 0), np.argmin(c, 0)

    def get_array(self, arr, mask, i, incr):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns).
            mask: np.array with shape (number of snippets, number of patterns).
            i: int, 0 <= i < number of patterns.
            add: bool.
        Returns:
            X1: modified np.array with shape (number of snippets, number of patterns).
        """

        X1 = arr.copy()
        X1[:, i] += incr[mask[:, i]]

        return X1

    def check_impact(self, X, model_input):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns) or
                (number of patterns, ).
        Returns:
            ranked: np.array with shape (number of snippets, number of patterns)
                of sorted patterns in non-increasing order for each snippet of
                code.
            acts: np.array with shape (number of snippets, ) of
            numbers of necessary actions for complexity's decrement.
            0 - do not modify the pattern, 1 - decrease by 1, 2 - increase by 1.
        """

        if X.ndim == 1:
            X = X.copy()
            X = np.expand_dims(X, axis=0)
        ncss = X[:, -1]
        X = X[:, :-1]

        k = X.shape[1]
        complexity = model_input.model.predict(X)
        importances = np.zeros(X.shape)
        actions = np.zeros(X.shape)
        acts_complexity = np.zeros((X.shape[1], 6))
        for i in range(k):
            nulls, not_nulls = self.divide_array(X, i)
            mask = not_nulls > 0
            dec_arr = self.get_array(not_nulls, mask, i, -1.0 / ncss[X[:, i] > 0])
            complexity_minus = model_input.model.predict(dec_arr)
            incr_arr = self.get_array(not_nulls, mask, i, 1.0 / ncss[X[:, i] > 0])
            complexity_plus = model_input.model.predict(incr_arr)
            c, number = self.get_minimum(complexity[X[:, i] > 0], complexity_minus, complexity_plus)
            importances[:, i][X[:, i] > 0] = complexity[X[:, i] > 0] - c
            actions[:, i][X[:, i] > 0] = number
            acts_complexity[i, 0] += (complexity_minus < complexity[X[:, i] > 0]).sum()
            acts_complexity[i, 1] += (complexity_minus > complexity[X[:, i] > 0]).sum()
            acts_complexity[i, 2] += (complexity_minus == complexity[X[:, i] > 0]).sum()
            acts_complexity[i, 3] += (complexity_plus < complexity[X[:, i] > 0]).sum()
            acts_complexity[i, 4] += (complexity_plus > complexity[X[:, i] > 0]).sum()
            acts_complexity[i, 5] += (complexity_plus == complexity[X[:, i] > 0]).sum()

        ranked = np.argsort(-1 * importances, 1)
        acts = actions[np.argsort(ranked, 1) == 0]
        return ranked, importances, acts_complexity, acts
