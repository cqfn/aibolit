import os
import pickle
from unittest import TestCase
from pathlib import Path
from aibolit.model.model import PatternRankingModel  # flake8: noqa


class TestArrayAsArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_test_function(self):
        files = [str(x.absolute()) for x in Path(self.dir_path, 'start_end').glob('*.java')]
        with open(Path(self.dir_path, 'model.pkl'), 'rb') as fid:
            model: PatternRankingModel = pickle.load(fid)

        results = model.test(files)
        print(results)
