#!/usr/bin/python3

import os
import shutil

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

def copy(fr: str, to: str, _file: bool=True):
    if not _file:
        shutil.copytree(base_dir + fr, to)
    else:
        shutil.copy2(base_dir + fr, to)
    print(f"copy: {fr} => {to} done...")

try:
    copy("kangaroo-app", "/usr/share/kangaroo-app", False)
    copy("kangaroo-uninstall", "/usr/bin/")
    copy("kangaroo", "/usr/bin/")
    copy("kangaroo.desktop", "/usr/share/applications/")
except PermissionError:
    print("! PermissionError: run this script as root or use sudo")
