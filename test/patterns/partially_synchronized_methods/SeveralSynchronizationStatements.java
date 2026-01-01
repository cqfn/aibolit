// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class SingleCLass {
    int synchronizationField = 0;

    // full synchronization can be achieved only by single 'synchronized' statement
    public void sequentialSynchronization() {
        synchronized(synchronizationField) {                            // pattern found this line
            int x = 0;
        }

        synchronized(synchronizationField) {                            // pattern found this line
            int y = 0;
        }
    }

    public void fullySynchronizedWithNestedSynchronization() {
        synchronized(synchronizationField) {
            int x = 0;

            synchronized(synchronizationField) {
                int y = 0;
            }
        }
    }

    public void partiallySynchronizedWithNestedSynchronization() {
        synchronized(synchronizationField) {                            // pattern found this line
            int x = 0;

            synchronized(synchronizationField) {                        // pattern found this line
                int y = 0;
            }
        }

        callSmt();
    }
}
