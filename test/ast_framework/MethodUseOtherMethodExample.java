// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
/**
* Some documentation
*/
class MethodUseOtherMethod {
    private int connectingField = 0;
    @SuppressWarnings("unused")
    private int redundantField = 0;

    public int useOnlyMethods1(int x) {
        if(x == 1) {
            return 1;
        }
        return 2 * useOnlyMethods2(x - 1);
    }

    public int useOnlyMethods2(int x) {
        if(x == 1) {
            return 1;
        }

        return 1 + useOnlyMethods1(x / 2);
    }

    public int getField() {
        return connectingField;
    }

    public void setField(int value) {
        connectingField = value;
    }

    public void standAloneMethod() {
            System.out.println("Stand alone");
    }

    public int shadowing(int redundantField) {
        return redundantField + 1;
    }
}
