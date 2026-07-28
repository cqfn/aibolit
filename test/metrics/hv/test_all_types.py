# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from subprocess import CompletedProcess, PIPE
from unittest.mock import patch

from aibolit.metrics.hv.main import HVMetric


class TestHVMetric:
    def test_run_analysis(self):
        file = 'test/metrics/cc/Complicated.java'
        metric = HVMetric(file)
        with patch(
                'aibolit.metrics.hv.main.subprocess.run',
                return_value=CompletedProcess(
                    args=['java', '-jar', str(HVMetric.jar_path), file],
                    returncode=0,
                    stdout=b'321.1728988800479\n'
                )
        ) as run:
            res = metric.value()
        run.assert_called_once_with(
            ['java', '-jar', str(HVMetric.jar_path), file],
            stdout=PIPE,
            check=True
        )
        assert res['data'][0]['halsteadvolume'] == 321.1728988800479
        assert res['data'][0]['file'] == file

    def test_run_analysis_does_not_call_maven(self):
        file = 'test/metrics/cc/Complicated.java'
        metric = HVMetric(file)
        with patch(
                'aibolit.metrics.hv.main.subprocess.run',
                return_value=CompletedProcess(args=[], returncode=0, stdout=b'1.0\n')
        ) as run:
            metric.value()
        command = run.call_args.args[0]
        assert command[:3] == ['java', '-jar', str(HVMetric.jar_path)]
        assert 'mvn' not in command
