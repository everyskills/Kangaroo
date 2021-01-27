#!/usr/bin/python3

import importlib

def Import(_file: str):
    spec = importlib.util.spec_from_file_location(_file, _file)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

if __name__ == "__main__":
    try:
        Import("/usr/share/Kangaroo/index.py").main()
    except Exception:
        print("! somthing error")