// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesExample {
    private final static String FILENAME = "file1.txt";

    public static void main(String[] args) {
		 new Thread() {

            @Override
            public void run() {
				super.method1();
                ArrayList<Boolean> list = new ArrayList<Boolean>();
                for (int i = 0; i < 10; i++)
                    for (int j = 0; j < 10; j++)
                        list.add(Boolean.FALSE);
            }
        }.start();
    }
}
