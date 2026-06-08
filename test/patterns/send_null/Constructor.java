// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

    private static class CompressionOption implements Option {
      private final CompressionType value;
      private final CompressionCodec codec;
      CompressionOption(CompressionType value) {
        this(value, null);
      }
      CompressionOption(CompressionType value, CompressionCodec codec) {
        this.value = value;
        this.codec = (CompressionType.NONE != value && null == codec)
          ? new DefaultCodec()
          : codec;
      }
      CompressionType getValue() {
        a.method_call(2, b.method_call(null));
        a.method_call().method_call(b).method_call(null);
        doSomething(myString = ( ( myString != 5) ? null : myString ), obj);
        doSomething(myString = ( ( myString != 5) ? myString.toLowerCase() : null), obj);
        new Object(null);
        return value;
      }
      CompressionCodec getCodec() {
        return codec;
      }
    }
