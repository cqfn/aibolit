// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class AnonymousClassProtectedMethod {

    // defining anonymous class
    AnonymousClassProtectedMethod object1 = new AnonymousClassProtectedMethod() {
       protected void protectedMethodAnonymous(){

       }
    };
}
