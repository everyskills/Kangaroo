<img src="icons/bg.jpg" align="right" />

# Awesome README

## Installation

```bash
git close https://www.github.com/everyskills/Kangaroo.git
unzip Kangaroo
cd Kangaroo
sudo chmod +x kangaroo
sudo python3 install.py
kangaroo
```

## Uninstall

open your terminal and execute this command

```bash
kangaroo-uninstall
```

## Plugin Usage
- use this tree for create plugin

```tree
|--+ plugin-name.ext
    |-- icon.png
    |-- main.py
    |-- package.json
```

- ```main.py```
```python
#!/usr/bin/python3
#-*- coding: utf-8 -*-#

import os

from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Plugin(QWidget):
    def __init__(self, line_edit, pkg, parent):
        super(Plugin, self).__init__()
        QWidget.__init__(self)

        self.input = line_edit # QLineEdit
        self.pkg = pkg         # built in functions
        self.parent = parent   # window built in functions
        self.ui = loadUi(base_dir + "designe.ui", self) # ui file

        ... # your code here
```

- ```package.json```
```json
{
	"name": "Plugin Name",
	"version": "1.0.0",
	"description": "example description",
	"icon": "icon.png",
	"help": "README.md",
	"key_word": "key word for start plugin",
	"script": "main.py",
	"author_name": "example",
	"author_email": "example@gmail.com",
	"home_page": "https://www.example.com",
	"author_description": "Python Developer"
}
```

## Start Usage
- open your app launcher
- selecte kangaroo
- now click in icon to show/hide<br>
<img src="icons/task_bar.png" align="top" /><br>

## How start work with plugin
- for start plugin write ```plugin:``` <br>
<img src="icons/start_plugin.gif" align="top" /><br>

- for end plugin and start another plugin write ```end:``` or ```clear:``` or ```cls:```
<img src="icons/end_plugin.gif" align="top" /><br>

## Built in Plugins
- files (v1.0.0)
- app   (v1.0.0)

## Shortcuts
| Hotkey  | Function
|:----: |----
| F       | Focus input line edit
| Ctrl+Q  | Quit app
| Esc     | Hide app

## System Supports
- [x] Linux
- [ ] MacOS
- [ ] Windows
