# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import subprocess
from pathlib import Path


def test_xcop_find_prunes_excluded_directories(tmp_path):
    (tmp_path / 'pom.xml').write_text('<project/>', encoding='utf-8')
    for directory in ('.venv', '.env', 'wp'):
        excluded = tmp_path / directory
        excluded.mkdir()
        (excluded / 'launcher manifest.xml').write_text('<xml/>', encoding='utf-8')

    result = subprocess.run(
        ['bash', '-c', _xcop_find_command()],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )

    assert result.stdout.splitlines() == ['./pom.xml']


def _xcop_find_command() -> str:
    makefile = Path(__file__).resolve().parents[1] / 'Makefile'
    for line in makefile.read_text(encoding='utf-8').splitlines():
        stripped = line.strip()
        if stripped.startswith('done < <(') and stripped.endswith(')'):
            return stripped.removeprefix('done < <(')[:-1]
    raise AssertionError('Cannot find xcop find command in Makefile')
