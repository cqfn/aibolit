// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class ScopeTest {

    /**
     * [Local variable, Local variable]
     */
    @SuppressWarnings("unused")
    void plain_method() {
        int x = 0;
        int y = 0;
    }

    /**
     * [Local variable, Assert statement]
     * |---[Binary operation]
     */
    void lambda_in_assert() {
        int array[] = {1, 2, 0};
        assert isSorted(array, (x, y) -> x < y);
    }

    /**
     * [Local variable, Block statement]
     * |---[Local variable]
     */
    @SuppressWarnings("unused")
    void nested_blocks() {
        int x = 0;

        {
            int y = 0;
        }
    }

    /**
     * [Local variable, Do statement, While statement, While statement, While statement]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Binary operation]
     * |---[Statement expression]
     */
    void while_cycle() {
        int x = 0;

        do {
            System.out.println(x);
        } while(x != 0);

        while(x != 0) {
            System.out.println(x);
        }

        while(x != 0)
            System.out.println(x);

        while(check(x -> x != 0, x))
            System.out.println(x);
    }

    /**
     * [Local variable, For statement, For statement, Local variable,
     *                  For statement, For statement, For statement]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Binary operation]
     * |---[Statement expression]
     */
    void for_cycle() {
        int x = 0;

        for(int y = 0; y < 10; y++) {
            System.out.println(y);
        }

        for(int y = 0; y < 10; y++)
            System.out.println(y);

        int array[] = {0, 1, 2};

        for(int elem: array) {
            System.out.println(elem);
        }

        for(int elem: array)
            System.out.println(elem);

        for(int y = 0; check(x -> x < 10, y); y++)
            System.out.println(y);
    }

    /**
     * [Local variable, If statement, If statement, If statement,
     *                  If statement, If statement, If statement]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Binary operation]
     * |---[Statement expression]
     */
    void if_branching() {
        int x = 0;

        if(x > 0) {
            System.out.println(x);
        }

        if(x > 0)
            System.out.println(x);

        if(x > 0) {
            System.out.println(x);
        } else {
            System.out.println(x);
        }

        if(x > 0)
            System.out.println(x);
        else
            System.out.println(x);

        if(x > 0) {
            System.out.println(x);
        } else if(x < 0) {
            System.out.println(x);
        } else {
            System.out.println(x);
        }

        if(check(x -> x > 0, x))
            System.out.println(x);
    }

    /**
     * [Local variable, Local variable, Local variable]
     * |---[Binary operation]
     * |---[Binary operation]
     */
    void local_variables() {
        int x = 0;

        int y = apply(x -> x + 1, 0);

        int z = 0, zz = apply(x -> x + 1, 0);
    }

    /**
     * [Local variable, Statement expression, Throw statement, Return statement]
     * |---[Binary operation]
     * |---[Member reference]
     * |---[Binary operation]
     */
    int statements_with_expressions() {
        int x = 0;

        apply(x -> x + 1, 0);

        throw new Object(x -> x);

        return apply(x -> x + 1, 0);
    }

    /**
     * [Local variable, Switch statement, Switch statement]
     * |---[Statement expression, Statement expression, Statement expression]
     * |---[Binary operation]
     * |---[Statement expression]
     */
    void switch_branching() {
        int x = 0;

        switch(x) {
            case 0:
                System.out.println(x);

            case 1:
            case 2:
                System.out.println(x);

            default:
                System.out.println(x);
        }

        switch(apply(x -> x + 1, x)) {
            default:
                System.out.println(x);
        }
    }

    /**
     * [Variable declaration, Synchronized statement, Synchronized statement]
     * |---[Statement expression]
     * |---[Class creator]
     * |---[Statement expression]
     */
    void synchronized_block() {
        Object obj = new Object();

        synchronized(obj) {
            System.out.println(obj);
        }

        synchronized(apply(s -> new Object(s), "string")) {
            System.out.println(obj);
        }
    }

    /**
     * [Try statement]
     * |---[Member reference]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     * |---[Statement expression]
     */
    void try_statement() {
        try(
            Object resource1 = new Object();
            Object resource2 = new Object(x -> x);
        ) {
            System.out.println(resource1);
        } catch(Error e) {
            System.out.println(e);
        } catch(OtherError e) {
            System.out.println(e);
        } finally {
            System.out.println("Finally");
        }
    }

    /**
     * [Local variable, Statement expression]
     * |---[Statement expression, Return statement]
     */
    void multiline_lambda() {
        int array[] = {1, 2, 3};
        Arrays.sort(array, (x, y) -> {
            System.out.println("Inside lambda");
            return x < y;
        });
    }

    /**
     * [For statement]
     * |---[If statement]
     *     |---[Assert statement]
     *         |---[Binary operation]
     */
    void deep_nesting() {
        for(int x = 0; x < 10; ++x) {
            if(x < 5) {
                assert check(x -> x < 5, x);
            }
        }
    }
}
