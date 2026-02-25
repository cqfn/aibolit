// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed.

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package com.huawei.codecheck.customchecks;

import com.puppycrawl.tools.checkstyle.api.AbstractCheck;
import com.puppycrawl.tools.checkstyle.api.DetailAST;
import com.puppycrawl.tools.checkstyle.api.TokenTypes;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 建议8.2.1 用括号明确表达式的操作顺序，避免过分依赖默认优先级
 * 一元操作符，不需要使用括号
 * 涉及位操作，推荐使用括号
 * 如果不涉及多种操作符，不需要括号
 * 对于极简的不会产生误解的三元表达式或者条件表达式，例如单个值（变量或常量)、函数调用的，可以不加括号 *
 */
public class ConditionalExpressionCheck extends AbstractCheck {
    private static final String MSG_CONDITIONAL_EXPRESSION = "ConditionalExpression";
//    Pattern LAND = Pattern.compile(".*\\)\\s*&&\\s*\\(.*");
//    Pattern LOR = Pattern.compile(".*\\)\\s*&&\\s*\\(.*");
    private Pattern pattern = Pattern.compile("^\\s*\\(.*\\)\\s*$");

    @Override
    public int[] getDefaultTokens() { return this.getAcceptableTokens(); }

    @Override
    public int[] getAcceptableTokens() {
        return new int[] { TokenTypes.BAND, TokenTypes.BNOT, TokenTypes.BOR, TokenTypes.BAND_ASSIGN,
                TokenTypes.BOR_ASSIGN, TokenTypes.BSR, TokenTypes.BSR_ASSIGN, TokenTypes.BXOR,
                TokenTypes.BXOR_ASSIGN, TokenTypes.UNARY_MINUS, TokenTypes.UNARY_PLUS };
    }

    @Override
    public int[] getRequiredTokens() { return this.getAcceptableTokens(); }

    @Override
    public void visitToken(DetailAST ast) {
        if ((ast.getPreviousSibling() != null && ast.getPreviousSibling().getType() == TokenTypes.LPAREN)
                || (ast.getNextSibling() != null && ast.getNextSibling().getType() == TokenTypes.RPAREN)) {
            // TO-FIX 还要排除(!a||~b)的情况

        }

        // 获得整个if表达式
        String[] codeLines = getLines();
        int ifLineNo = ast.getLineNo();
        DetailAST exprAst = ast.getFirstChild().getNextSibling();
        if(exprAst == null) {
            return;// TO-FIX ???
        }
        int exprLineNo = exprAst.getLineNo();
        String ifExpression = codeLines[ifLineNo - 1].trim();
        if (exprLineNo > ifLineNo) {
            for (int i = ifLineNo ; i < exprLineNo; i++) {
                ifExpression = ifExpression + codeLines[i].trim();
            }
        }

        boolean needWarning = false;
        if (ifExpression.contains("&&") || ifExpression.contains("||")) {
            String[] conditionalExpressions = ifExpression.split("&&|\\|\\|");
            int conditionsNo = conditionalExpressions.length;
            if (conditionsNo == 2) {
                if (!conditionalExpressions[0].trim().endsWith(")") || !conditionalExpressions[1].trim().startsWith("(")) {
                    needWarning = true;
                }
            } else if (conditionsNo >= 3) {
                int i = conditionsNo - 1;
                if (!conditionalExpressions[0].trim().endsWith(")") || !conditionalExpressions[i].trim().startsWith("(")) {
                    needWarning = true;
                }
                for (int a = 1; a < i; a++) {
                    Matcher matcher = pattern.matcher(conditionalExpressions[a]);
                    if (!matcher.find()) {
                        needWarning = true;
                    }
                }
            }
        }
        if (needWarning) {
            log(ast.getLineNo(), ast.getColumnNo(), MSG_CONDITIONAL_EXPRESSION, ast.getText());
        }
    }
}
