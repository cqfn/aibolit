# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from textwrap import dedent
from unittest import TestCase

from aibolit.metrics.cognitiveC.cognitive_c import CognitiveComplexity
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


class CognitiveComplexityTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test1(self):
        filepath = self.current_directory / '1.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 7)

    def test2(self):
        filepath = self.current_directory / '2.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 9)

    def test3(self):
        filepath = self.current_directory / '3.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 10)

    def test4(self):
        filepath = self.current_directory / '4.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 6)

    def test5(self):
        filepath = self.current_directory / '5.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 3)

    def test6(self):
        filepath = self.current_directory / '6.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 14)

    def test7(self):
        filepath = self.current_directory / 'recursion.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 6)

    def test8(self):
        filepath = self.current_directory / 'nested.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 9)

    def test9(self):
        filepath = self.current_directory / '7.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 17)

    def test10(self):
        filepath = self.current_directory / '8.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 13)

    def test_co_co_sonar_guide_example_1(self):
        content = dedent(
            '''\
            class Dummy {
              // See: https://www.sonarsource.com/docs/CognitiveComplexity.pdf Appendix C
              private static String toRegexp(String antPattern, String directorySeparator) {
                final String escapedDirectorySeparator = '\\\\' + directorySeparator;
                final StringBuilder sb = new StringBuilder(antPattern.length());
                sb.append('^');
                int i = antPattern.startsWith("/") ||                        // +1
                     antPattern.startsWith("\\\\") ? 1 : 0;                  // +1
                while (i < antPattern.length()) {                            // +1
                  final char ch = antPattern.charAt(i);
                  if (SPECIAL_CHARS.indexOf(ch) != -1) {                     // +2 (nesting = 1)
                    sb.append('\\\\').append(ch);
                  } else if (ch == '*') {                                    // +1
                    if (i + 1 < antPattern.length()                          // +3 (nesting = 2)
                            && antPattern.charAt(i + 1) == '*') {            // +1
                      if (i + 2 < antPattern.length()                        // +4 (nesting = 3)
                           && isSlash(antPattern.charAt(i + 2))) {           // +1
                        sb.append("(?:.*")
                            .append(escapedDirectorySeparator).append("|)");
                        i += 2;
                      } else {                                               // +1
                        sb.append(".*");
                        i += 1;
                      }
                    } else {                                                 // +1
                      sb.append("[^").append(escapedDirectorySeparator).append("]*?");
                    }
                  } else if (ch == '?') {                                    // +1
                    sb.append("[^").append(escapedDirectorySeparator).append("]");
                  } else if (isSlash(ch)) {                                  // +1
                    sb.append(escapedDirectorySeparator);
                  } else {                                                   // +1
                    sb.append(ch);
                  }
                  i++;
                }
                sb.append('$');
                return sb.toString();
              }
            }                                                                // total = 20
            '''
        ).strip()
        self.assertEqual(CognitiveComplexity().value(
            AST.build_from_javalang(
                build_ast_from_string(content),
            ),
        ), 20)
