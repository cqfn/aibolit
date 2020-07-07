import java.util.Collections;       // +0
import java.io.IOException;         // +0

class Foo {                         // +1, total Ncss = 16
  
  public void bigMethod()           // +1
      throws IOException {     
    int x, y = 2;               // +1
    boolean a, b;               // +1
    a = false;                  // +1
    b = true;                   // +1 
    x = 0;                      // +1
    if (a || b) {                   // +1
      try {                         // +1
        do {                        // +1
          x += 2;                   // +1
        } while (x < 12);
          
        System.exit(0);             // +1
      } catch (IOException ioe) {   // +1
        throw new PatheticFailException(ioe); // +1
      } finally {                   // +1
        System.out.println("Finally Block");
      }
    } else {
      assert false;                 // +1
    }
  }     
}
