// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class NoJoinedValidation {
    void print(int x, int y) {
        if (x == 1 || y != 1) {
            if (true) { // -> false case, since we have if, we need only throw
                throw new Exception("Oops");
            }
        }
    }
    //test 'ReturnStatement' object has no attribute 'statements' case
    int returnStatement(int x, int y) {
        if (x == 1 || y != 1)
            return x + y;
        return 0;
    }
    //test 'StatementExpression' object has no attribute 'statements' case
    int statementExpression(int x, int y) {
        if (x < 0 || y >= 0 && x < y)
            x = y;
        return 0;
    }
    //test 'ContinueStatement' object has no attribute 'statements' case
    int continueStatement(int z) {
        for (int i=0; i<10; i++){
            if (i > z) continue;
        }
        return 0;
    }
    //test 'DoStatement' object has no attribute 'statements' case
    int doStatement(int i) {
        if (i < 100)
            do {
                i = i + 1;
            } while (
                i < 100
            );
        return i;
    }
    //test 'BreakStatement' object has no attribute 'statements' case
    int breakStatement(int z) {
        for (int i=0; i<10; i++){
            if (i > z) break;
        }
        return 0;
    }
    //test 'ForStatement' object has no attribute 'statements' case
    int forStatement(int z) {
        if (z > 0)
            for (int i=0; i<10; i++)
                z++;
         return 0;
    }
    //test 'IfStatement' object has no attribute 'statements' case
    void ifStatement(int z) {
        if (z > 0) return;
    }
    //test 'SwitchStatement' object has no attribute 'statements' case
    int switchStatement(int z) {
        int a = 0;
        if (z > 0)
            switch(z){
                case 1:
                    a = 3;
                    break;
                case 2:
                    a = 4;
                    break;
                default:
                    a = 5;
            }
        return a;
    }
}
