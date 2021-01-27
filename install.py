#!/usr/bin/python3

import os
import shutil

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

try:
    shutil.copytree(base_dir + "app", "/usr/share/Kangaroo")
    shutil.copy2(base_dir + "kangaroo-uninstall.py", "/usr/bin/")
    shutil.copy2(base_dir + "kangaroo.py", "/usr/bin/")
    shutil.copy2(base_dir + "kangaroo.desktop", "/usr/share/applications/")
except PermissionError:
    print("! PermissionError: run this script as root or use sudo")
