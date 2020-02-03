from unittest import TestCase
from aibolit.metrics.loc import Loc


class LocTest(TestCase):
    def test_it_works(self):
        m = Loc('test')
        m.value()
        print('Works just fine!')
