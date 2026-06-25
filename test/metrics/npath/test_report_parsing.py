# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import pytest

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
    """PMD error entries should still surface as exceptions."""
    with pytest.raises(Exception, match='PMDException'):
        NPathMetric.parse_report(
            '''
            <pmd>
              <error filename="/tmp/npath/src/main/java/test/metrics/npath/ooo.java"
                     msg="PMDException" />
            </pmd>
            ''',
            '/tmp/npath',
        )
