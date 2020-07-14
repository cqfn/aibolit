class MultipleWhile {
  void bar() {
    while (true) {
      x = 1;
    }
    // more code
    if (true) {
        while (false) {
          x = 1;
        }
    }
  }
}