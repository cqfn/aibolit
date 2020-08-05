import os
import pickle
from unittest import TestCase
from pathlib import Path

from aibolit.config import Config
from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument


class TestArrayAsArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = ArrayAsArgument()

    def test_test_function(self):
        files = [str(x.absolute()) for x in Path(self.dir_path, 'start_end').glob('*.java')]
        model_path = Config.folder_model_data()
        with open(model_path, 'rb') as fid:
            model = pickle.load(fid)

        results = model.test(files)
        print(results)
        # self.assertEqual(
        #     [],
        #     self.pattern.value(file),
        #     'Should not match no argument method'
        # )
