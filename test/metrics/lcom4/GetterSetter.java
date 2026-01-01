// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

public class GetterSetter {

    private int a;
    private int b;

    public String getName(){
      return name;
    }

    public Object getResource() {
      return resource;
    }

    public void doNothing() {
        this.a++;
        this.b++;
        System.out.println(this.a + this.b);
        int i = 0;
        if (i < this.a) {
            return 0;
        } else {
            return 1;
        }
    }

}
