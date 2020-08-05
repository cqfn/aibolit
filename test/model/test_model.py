import os
import pickle
from unittest import TestCase
from pathlib import Path

from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument


class TestArrayAsArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = ArrayAsArgument()

    def test_test_function(self):
        files = [str(x.absolute()) for x in Path(self.dir_path, 'start_end').glob('*.java')]
        with open('model.pkl', 'rb') as fid:
            model = pickle.load(fid)

        results = model.test(files)
        print(results)
