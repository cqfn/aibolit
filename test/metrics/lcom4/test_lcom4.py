# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path
from aibolit.metrics.lcom4.lcom4 import LCOM4


class TestLCOM4(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = LCOM4()

    def test_class_with_empty_method(self):
        name = 'EmptyMethod.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 2)

    def test_constructor(self):
        name = 'Constructor.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 1)

    def test_scope_with_anonymous(self):
        name = 'ScopeAnonymous.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 2)

    def test_simple(self):
        name = 'Simple.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 1)

    def test_getter_setter(self):
        name = 'GetterSetter.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        # We should ignore all setters and getters
        self.assertEqual(lcom4_val, 1)

    def test_scope(self):
        name = 'Scope.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 2)

    def test_overloaded(self):
        name = 'Overloaded.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 1)

    def test_class_with_chain(self):
        name = 'MethodChain.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 2)

    def test_overloaded_diff(self):
        name = 'OverloadedDiffComp.java'
        lcom4_val = self.pattern.value(Path(self.dir_path, name))
        self.assertEqual(lcom4_val, 1)
