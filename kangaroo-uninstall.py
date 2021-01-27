#!/usr/bin/python3

import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

try:
    os.rmdir("/usr/share/Kangaroo")
    os.remove("/usr/share/applications/kangaroo.desktop")
    os.remove("/usr/bin/kangaroo.py")
    os.remove("/usr/bin/kangaroo-uninstall.py")
except PermissionError:
    print("! PermissionError: run this script as root or use sudo")
