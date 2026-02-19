# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from aibolit.__main__ import print_total_score_for_file


def test_print_total_score_for_file_handles_missing_results_key():
    buffer = []
    totals = []
    out = print_total_score_for_file(buffer, 'A.java', totals, {})

    assert out == {}
    assert totals == [0.0]
    assert buffer == ['A.java score: 0.00']
