# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import sys
import subprocess
import time
import signal


def test_quiet_exiting():
    proc = subprocess.Popen(
        [sys.executable, 'aibolit'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)
    proc.send_signal(signal.SIGINT)

    stdout, stderr = proc.communicate(timeout=3)
    combined = stdout + stderr

    assert b'Traceback' not in combined
    assert b'KeyboardInterrupt' not in combined
