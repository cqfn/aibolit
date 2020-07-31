import pickle
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
from aibolit.config import Config
from aibolit.model.model import PatternRankingModel, scale_dataset, get_minimum  # noqa: F401 type: ignore


class Stats(object):

    @staticmethod
    def aibolit_stat(test_csv: pd.DataFrame, model=None) -> pd.DataFrame:
        if not model:
            load_model_file = Config.folder_model_data()
            print('Loading model from file {}:'.format(load_model_file))
            with open(load_model_file, 'rb') as fid:
                model = pickle.load(fid)
                print('Model has been loaded successfully')

        scaled_dataset = scale_dataset(test_csv, model.features_conf)
        cleaned_dataset = scaled_dataset[model.features_conf['features_order'] + ['M2']]
        ranked, _, acts_complexity, acts = Stats.check_impact(
            cleaned_dataset.values,
            model
        )

        m, p = Stats.count_acts(acts, ranked)
        return Stats.get_table(model.features_conf['features_order'], m, p, acts_complexity)

    @staticmethod
    def count_acts(
            acts: np.array,
            ranked: np.array) -> Tuple[np.array, np.array]:
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

    @staticmethod
    def get_patterns_name() -> Dict[Any, Any]:
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

    @staticmethod
    def get_table(
            features_conf: Dict[Any, Any],
            m: np.array,
            p: np.array,
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
        replace_dict = Stats.get_patterns_name()
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

    @staticmethod
    def split_dataset_by_pattern_value(
            X: np.array,
            pattern_idx: int) -> Tuple[np.array, np.array]:
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

    @staticmethod
    def change_matrix_by_value(
            arr: np.array,
            mask: np.array,
            i: int,
            incr: np.array):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns).
            mask: np.array with shape (number of snippets, number of patterns).
            i: int, 0 <= i < number of patterns.
            incr: matrix values to add.
            mask: matrix of bools
        Returns:
            X1: modified np.array with shape (number of snippets, number of patterns).
        """

        X1 = arr.copy()
        X1[:, i] += incr[mask[:, i]]

        return X1

    @staticmethod
    def check_impact(
            X: np.array,
            model_input: Any):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns) or
                (number of patterns, ).
            model_input: model to use
        Returns:
            ranked: np.array with shape (number of snippets, number of patterns)
                of sorted patterns in non-increasing order for each snippet of
                code.
            acts: np.array with shape (number of snippets, ) of
            numbers of necessary actions for complexity's decrement.
            0 - do not modify the pattern, 1 - decrease by 1, 2 - increase by 1.
            importances: importances of patters
            acts_complexity: matrix with number of time for each pattern when:
                pattern was increased, complexity increased,
                pattern was increased, complexity decreased, etc.
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
            nulls, not_nulls = Stats.split_dataset_by_pattern_value(X, i)
            mask = not_nulls > 0
            dec_arr = Stats.change_matrix_by_value(not_nulls, mask, i, -1.0 / ncss[X[:, i] > 0])
            complexity_minus = model_input.model.predict(dec_arr)
            incr_arr = Stats.change_matrix_by_value(not_nulls, mask, i, 1.0 / ncss[X[:, i] > 0])
            complexity_plus = model_input.model.predict(incr_arr)
            c, number = get_minimum(complexity[X[:, i] > 0], complexity_minus, complexity_plus)
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
