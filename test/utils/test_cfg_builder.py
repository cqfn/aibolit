# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path

from aibolit.ast_framework.java_package import JavaPackage


class CFGBuilderTestCase(TestCase):

    def test_cfg_of_method(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'SimpleClass.java')
        java_class = java_package.java_classes['Simple']
        methods = java_class.methods['Increment']
        self.assertEqual(len(methods), 1)
        method = next(iter(methods))
        self.assertEqual(method.cfg.size(), 2)
