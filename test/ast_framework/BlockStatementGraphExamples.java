class BlockStatementGraphExamples {
    void singleAssertStatement(int x) {
        assert x == 0;
    }

    int singleReturnStatement(int x) {
        return x;
    }

    void singleStatementExpression(int x) {
        x += 1;
    }

    void singleThrowStatement(int x) {
        throw x;
    }

    void singleVariableDeclarationStatement() {
        int x;
    }

    int singleBlockStatement(int x) {
        {
            return x;
        }
    }

    void singleDoStatement(int x) {
        do{
            x--;
        } while(x > 0);
    }

    void singleForStatement(int x) {
        for(int i = 0; i < 10; ++i) {
            x += 1;
        }
    }

    void singleSynchronizeStatement(int x) {
        synchronized(x) {
            x += 1;
        }
    }

    void singleWhileStatement(int x) {
        while(x > 0) {
            x--;
        }
    }

    void cycleWithBreak(int x) {
        while(x > 0) {
            break;
        }
    }

    void cycleWithContinue(int x) {
        while(x > 0) {
            continue;
        }
    }

    void singleIfThenBranch(int x) {
        if(x > 0) {
            x += 1;
        }
    }

    void singleIfThenElseBranches(int x) {
        if(x > 0) {
            x += 1;
        } else {
            x -= 1;
        }
    }

    void severalElseIfBranches(int x) {
        if(x > 0) {
            x += 1;
        } else if(x == 0) {
            x = 0;
        } else {
            x -= 1;
        }
    }

    int ifBranchingWithoutCurlyBraces(int x) {
        if(x > 0)
            return x;
        else
            return -x;
    }

    void switchBranches(int x) {
        switch(x) {
            case 0:
                x = 1;
                System.out.println(x);

            case 1: {
                x = 0;
            }
            System.out.println(x);

            default:
                x = -1;
        }
    }

    void singleTryBlock(Exception e) {
        try {
            throw e;
        }
        catch(Exception e) {
            System.out.println(e);
        }
    }

    void fullTryBlock(Exception e) {
        try(Resource resource = initResource() ) {
            throw e;
        }
        catch(OSException e) {
            System.out.println(e);
        }
        catch(Exception e) {
            System.out.println(e);
        }
        finally {
            System.out.println("FINALLY!!!");
        }
    }

    void tryWithoutCatch(Exception e) {
        try {
            throw e;
        }
        finally {
        }
    }

    void complexExample1(int x) {
        x += 1;

        for(int i = 0; i < x; ++i) {
            x--;
        }

        while(x > 0) {
            x--;
        }

        return x;
    }
}
