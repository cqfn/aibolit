# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import subprocess
import signal
import time
import sys


def test_graceful_shutdown():
    process = subprocess.Popen(
        [sys.executable, '-m', 'aibolit', 'check', '--folder', 'test'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    time.sleep(3)
    launched = False
    start_time = time.time()
    timeout = 10

    while time.time() - start_time < timeout:
        line = process.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue

        if 'aibolit has been launched' in line:
            launched = True
            break

    if not launched:
        process.kill()
        raise AssertionError("Process didn't print launch message within timeout")

    process.send_signal(signal.SIGINT)

    try:
        _, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        _, stderr = process.communicate()
        assert False, "Process doesn't exit after SIGINT"

    assert 'KeyboardInterrupt' not in stderr
    assert 'Traceback' not in stderr
