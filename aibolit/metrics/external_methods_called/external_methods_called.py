# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT


class ExternalMethodsCalled:
    """
        Measure the number of external methods called by the class.
        @todo #183:30min Implement external method called metric
         In the methods in the class an external method for this class can
         be called. So number of external methods called by all the methods
         in the class is suggested as a metric. Implement this metric and then
         enable tests in test_external_methods_called.py
    """

    def __init__(self):
        pass

    def value(self, filename: str):
        return 0
