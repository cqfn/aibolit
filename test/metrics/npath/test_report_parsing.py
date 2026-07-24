# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import pytest

from aibolit.metrics.npath import main as npath_main
from aibolit.metrics.npath.main import NPathMetric


def test_parse_report_reads_complexity_from_xml():
    """PMD XML content should be parsed without touching the filesystem."""
    result = NPathMetric.parse_report(
        '''
        <pmd>
          <file name="/tmp/npath/src/main/java/test/metrics/npath/Foo.java">
            <violation>NPath complexity of 200</violation>
          </file>
        </pmd>
        ''',
        '/tmp/npath',
    )

    assert result == {
        'data': [{'file': 'test/metrics/npath/Foo.java', 'complexity': 200}],
        'errors': [],
    }


def test_parse_report_raises_pmd_error():
    """PMD error entries should surface with source-relative filenames."""
    with pytest.raises(Exception, match='test/metrics/npath/ooo.java: PMDException'):
        NPathMetric.parse_report(
            '''
            <pmd>
              <error filename="/tmp/npath/src/main/java/test/metrics/npath/ooo.java"
                     msg="PMDException" />
            </pmd>
            ''',
            '/tmp/npath',
        )


def test_parse_report_raises_on_malformed_violation():
    """Unexpected violation text should fail with a descriptive parser error."""
    with pytest.raises(ValueError, match='Unexpected PMD violation format'):
        NPathMetric.parse_report(
            '''
            <pmd>
              <file name="/tmp/npath/src/main/java/test/metrics/npath/Foo.java">
                <violation>unexpected</violation>
              </file>
            </pmd>
            ''',
            '/tmp/npath',
        )


def test_parse_report_normalizes_windows_source_paths():
    """Windows-style PMD paths should still be trimmed to source-relative names."""
    result = NPathMetric.parse_report(
        '''
        <pmd>
          <file name="C:\\tmp\\npath\\src\\main\\java\\test\\metrics\\npath\\Foo.java">
            <violation>NPath complexity of 200</violation>
          </file>
        </pmd>
        ''',
        'C:\\tmp\\npath',
    )

    assert result == {
        'data': [{'file': 'test/metrics/npath/Foo.java', 'complexity': 200}],
        'errors': [],
    }


def test_value_preserves_root_initialization_error(monkeypatch):
    """Temporary-root setup errors should not be masked by cleanup."""
    metric = NPathMetric('Foo.java')

    def fail_gettempdir():
        raise RuntimeError('temp root failed')

    monkeypatch.setattr(npath_main.shutil, 'which', lambda _: 'mvn')
    monkeypatch.setattr(npath_main.tempfile, 'gettempdir', fail_gettempdir)

    with pytest.raises(RuntimeError, match='temp root failed'):
        metric.value()
