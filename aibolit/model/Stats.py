import pickle
import tarfile
from pathlib import Path
import numpy as np
import pandas as pd
from aibolit.config import Config
from aibolit.model.model import Dataset, TwoFoldRankingModel  # type: ignore


class Stats():

    def stats(self):
        dataset_archive = Config.get_dataset_file()
        # archive = tarfile.open("datasets.tar.gz", "w|gz")
        # for f in files:
        #     print(str(f), f.name)
        #     archive.add(str(f), arcname=f.name)
        # archive.close()
        try:
            tar = tarfile.open(str(dataset_archive))
            tar.extractall(path=dataset_archive.parent)
            tar.close()
            print('Dataset has been unzipped successfully')
        except Exception as e:
            print('Dataset unzip failed: {}'.format(str(e)))
            return 1

        test_csv = pd.read_csv(Path(dataset_archive.parent, 'test.csv'), header=None)
        load_model_file = Config.folder_model_data()
        print('Test loaded model from file {}:'.format(load_model_file))
        with open(load_model_file, 'rb') as fid:
            model = pickle.load(fid)
            print('Model has been loaded successfully')
        ranked, _, acts_complexity, acts = self.check_impact(
            test_csv.values,
            model,
            scale=True,
            return_acts=True
        )

        m, p = self.count_acts(acts, ranked)
        self.print_table(model.feature_order, m, p, acts_complexity)

    def count_acts(self, acts, ranked):
        k = ranked[:, 0]
        m = np.zeros(ranked.shape[1])
        p = np.zeros(ranked.shape[1])
        for i in range(len(k)):
            if acts[i] == 1:
                m[k[i]] += 1
            elif acts[i] == 2:
                p[k[i]] += 1
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

    def print_table(self, features_conf, m, p, acts_complexity):
        def f(k):
            if k >= 10000:
                return 5
            elif k >= 1000:
                return 4
            elif k >= 100:
                return 3
            elif k >= 10:
                return 2
            else:
                return 1

        replace_dict = self.get_patterns_name()
        print("p+ : pattern_increase")
        print("p- : pattern_decrease")
        print("c+ : complexity_increase")
        print("c- : complexity_decrease")
        print("c= : complexity_no_change")
        print(
            "_______________________________________________________________________________________________________________________")
        print(
            "patterns                               |-1(top1) |+1(top1) |  p- c-  |  p+ c+  |  p- c+  |  p+ c-  |  p- c=  |  p+ c=  |")
        print(
            "_______________________________________________________________________________________________________________________")

        for i in range(len(features_conf)):
            a = int(m[i])
            b = int(p[i])
            p1 = int(acts_complexity[i, 0])
            p2 = int(acts_complexity[i, 4])
            p3 = int(acts_complexity[i, 1])
            p4 = int(acts_complexity[i, 3])
            p5 = int(acts_complexity[i, 2])
            p6 = int(acts_complexity[i, 5])
            pattern = replace_dict.get(features_conf[i])
            print(pattern, ' ' * (37 - len(pattern)), '|', a, ' ' * (6 - f(a)), '|', b, ' ' * (6 - f(b)), '|', p1,
                  ' ' * (6 - f(p1)),
                  '|', p2, ' ' * (6 - f(p2)), '|', p3, ' ' * (6 - f(p3)), '|', p4, ' ' * (6 - f(p4)), '|', p5,
                  ' ' * (6 - f(p5)), '|',
                  p6, ' ' * (6 - f(p6)), '|')

    def divide_array(self, X, pattern_idx):
        nulls = []
        not_nulls = []
        for snipp in X:
            if snipp[pattern_idx] == 0:
                nulls.append(snipp)
            else:
                not_nulls.append(snipp)

        return np.array(nulls), np.array(not_nulls)

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

    def check_impact(self, X, model_input, scale=True, return_acts=False):
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
        if scale:
            X = X[:, :-1] / ncss.reshape((-1, 1))
        else:
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
        if not return_acts:
            return ranked, importances, acts_complexity
        acts = actions[np.argsort(ranked, 1) == 0]
        return ranked, importances, acts_complexity, acts
