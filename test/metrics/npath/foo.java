        public class Foo {
          public static void bar() {
            boolean a, b = true;
            int j = 0;
            switch (j) { // 5
              case 0:
              case 1:
              case 3: if (a || b) {} break;
            }
            switch (j) { // * 5
              case 0:
              case 1:
              case 3: if (a || b) {} break;
            }
            if (true || a && b); // * 4
            while (j++ < 20);    // * 2
          }
        }
