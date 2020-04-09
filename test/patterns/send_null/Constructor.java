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
        return value;
      }
      CompressionCodec getCodec() {
        return codec;
      }
    }