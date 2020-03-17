import java.util.Collections;       // +0
import java.io.IOException;         // +0

class Foo {                         // +1, total Ncss = 12
  
  public void bigMethod()           // +1
      throws IOException {     
    int x = 0, y = 2;               // +1
    boolean a = false, b = true;    // +1
    
    if (a || b) {                   // +1
      try {                         // +1
        do {                        // +1
          x += 2;                   // +1
        } while (x < 12);
          
        System.exit(0);             // +1
      } catch (IOException ioe) {   // +1
        throw new PatheticFailException(ioe); // +1
      }
    } else {
      assert false;                 // +1
    }
  }     
}
