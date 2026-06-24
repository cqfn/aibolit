# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import io
import sys
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch

from aibolit.__main__ import run_parse_args


class TestCliHelp(TestCase):
    def test_usage_lists_registered_commands(self):
        commands = {
            'train': lambda: 0,
            'recommend': lambda: 0,
            'version': lambda: 0,
        }
        output = io.StringIO()

        with patch.object(sys, 'argv', ['aibolit', 'unknown']), redirect_stdout(output):
            with self.assertRaises(SystemExit) as raised:
                run_parse_args(commands)

        self.assertEqual(raised.exception.code, 1)
        usage = output.getvalue()
        self.assertIn('You can run 3 commands:', usage)
        self.assertIn('train          Train model', usage)
        self.assertIn('recommend      Recommend pattern', usage)
        self.assertIn('version        Show version', usage)
