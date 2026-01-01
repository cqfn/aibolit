# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.non_final_argument.non_final_argument import NonFinalArgument


class NonFinalArgumentTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_argument_in_ctor(self):
        self.assertEqual(
            NonFinalArgument().value(Path(self.dir_path, 'NonFinalArgumentCtor.java')), [10]
        )

    def test_find_non_final_argument_in_method(self):
        self.assertEqual(
            NonFinalArgument().value(Path(self.dir_path, 'NonFinalArgumentMethod.java')), [14]
        )
