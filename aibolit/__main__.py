#!/usr/bin/env python
"""The main entry point. Invoke as `aibolit' or `python -m aibolit'.
"""
import sys

def main():
    try:
        print('Hello, world!')
        exit_status = 0
    except KeyboardInterrupt:
        exit_status = ExitStatus.ERROR_CTRL_C
    sys.exit(exit_status)

if __name__ == '__main__':
    main()
