
import os
from unittest import TestCase
from aibolit.patterns.non_final_attribute.non_final_attribute import NonFinalAttribute
from pathlib import Path


class TestNonFinalAttribute(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_atributes(self):
        lines = NonFinalAttribute().value(Path(self.dir_path, 'NonFinalAttribute.java'))
        self.assertEqual(len(lines), 4)
