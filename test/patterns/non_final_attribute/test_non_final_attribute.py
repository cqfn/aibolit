
import os
from unittest import TestCase
from aibolit.patterns.non_final_attribute.non_final_attribute import NonFinalAttribute
from pathlib import Path


class TestSetter(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    non_final = NonFinalAttribute()

    def test_find_non_final_atributes(self):
        lines = self.non_final.value(Path(self.dir_path, 'NonFinalAttribute.java'))
        self.assertEqual(len(lines), 4)
