# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import subprocess
import time
import signal


def test_absence_traceback():
    proc = subprocess.Popen(
        ["python", "aibolit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(2)
    proc.send_signal(signal.SIGINT)
    stdout, _ = proc.communicate(timeout=3)

    assert b"Traceback" not in stdout
