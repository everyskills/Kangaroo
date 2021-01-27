#!/usr/bin/python3
#-*- coding: utf-8 -*-


"""
## COMMAND LINE

@Arguments: (ext)
    @Options: (ext)
        - install
        - remove
        - delete
        - run
        - show
        - update
        - open

@Arguments: (kang)
    @Options: (kang)
        - settings
        - plugins
        - themes
        - cmd

## Examples:
> ext [OPTIONS] value
> kang [OPTIONS] value
"""

import os
import json
import _pkg

from glob import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QLineEdit, QMenu, QStackedWidget, QSystemTrayIcon, QWidget
from PyQt5.uic import loadUiType
from _settings import MainWindowSettings
from _methods import  Controls

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")
app_ui, _ = loadUiType(base_dir + "ui/main.ui")

class MainWindow(QWidget, app_ui):
    
    global_vars = {}

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        
        self.def_setup = MainWindowSettings(self)
        self.def_setup.init_setup()
        self.def_setup.small_size()

        self.ClearSessionAction = QAction("Clear session", self, shortcut="Ctrl+W", triggered=self.reset_input)
        self.input.addAction(self.ClearSessionAction)
        
        self.stackedWidget = QStackedWidget()
        self.main_grid_layout.addWidget(self.stackedWidget)

        self.setWindowIcon(QIcon(base_dir + "icons/logo.png"))

        self.exts = {}
        self.count = 0

        self.set_plugins()           # search and get all plugins information
        # self.set_plugins_widgets() # for set all plugins
        self.input.textChanged.connect(self.set_plugin)
        self.input.textChanged.connect(self.search_plugin)
        # self.input.returnPressed.connect(self.command_manager)

        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()

        self.set_input_focus()

    def set_plugins(self):
        for d in glob(base_dir + "exts/*.ext/package.json"):
            script = self.get_json_value(d, "script", "main.py")
            path = os.path.dirname(d) + "/" + script
            kw = str(self.get_json_value(d, "key_word")).strip()

            if (kw and script and path):
                self.exts.update({kw: (self.count, _pkg.Import(path).Plugin, os.path.dirname(d) + "/")})
                self.count += 1

    def get_json_value(self, _file: str, key: str, value: str=""):
        return json.load(open(str(_file))).get(key.lower(), value)

    def set_plugin(self, text: str):
        kw = text.rstrip(":").strip()
        is_ext = text.endswith(":")

        if is_ext and kw in ("end", "clear", "cls"):
            self.def_setup.small_size()
            self.reset_input()
            self.input.addAction(self.ClearSessionAction)

        elif is_ext and kw in ("exit", "quit"):
            self.close()
            self.input.clear()

        elif is_ext and kw in ("update", "reload"):
            self.set_plugins()
            self.input.clear()

        elif is_ext and kw in list(self.exts.keys()):
            self.run_plugin(kw)

    def reset_input(self):
        ## delete last input
        self.gridLayout_2.removeWidget(self.input)
        self.input.deleteLater()

        ## get new input line without any event
        self.set_new_line()

        ## default setup for line input
        self.def_setup.remove_session()
        self.set_input_focus()

    def set_new_line(self):
        ## create line edit by object name input
        self.input = QLineEdit(self)
        self.input.setObjectName("input")

        ## add line to layout
        self.gridLayout_2.addWidget(self.input, 0, 1, 1, 1)
        
        ## set default setup for line
        self.def_setup.input_setup()

        ## connects functions
        # self.input.returnPressed.connect(self.command_manager)
        self.input.textChanged.connect(self.search_plugin)
        self.input.textChanged.connect(self.set_plugin)
        
    def set_plugins_widgets(self):
        for _, v in self.exts.items():
            self.stackedWidget.addWidget(v[1](self.input))

    def set_widget_by_name(self, name: str=""):
        self.stackedWidget.setCurrentIndex(self.exts[name][0])

    def get_ext_value(self, ext: str, key: str="", value: str=""):
        root_path = self.exts[ext][2]
        return self.get_json_value(root_path + "package.json", key, value), root_path

    def search_plugin(self, text: str):
        kw = text.rstrip(":").strip()
        is_ext = text.endswith(":")

        if is_ext and kw in list(self.exts.keys()):
            self.run_plugin(kw)

    def run_plugin(self, key_word: str):
        path = self.exts[key_word][2]
        icon = QIcon(path + self.get_ext_value(key_word, "icon")[0])

        self.input.clear()
        self.input.setPlaceholderText(f"Session: {key_word}")
        
        self.btn_ext.setText(key_word)
        self.btn_ext.setIcon(icon)

        control = Controls(self)
        self.stackedWidget.insertWidget(0, self.exts[key_word][1](self.input, _pkg, control))
        self.stackedWidget.setCurrentIndex(self.exts[key_word][0])

        self.def_setup.larg_size()
        self.set_input_focus()

    def createActions(self):
        self.hideAction = QAction("H&ide/S&how", self, shortcut="Alt+Space", triggered=self.check_win)
        self.quitAction = QAction(_pkg.get_sys_icon("application-exit"), "&Quit", self, triggered=QApplication.instance().quit)
        # self.showAction = QAction("S&how", self, shortcut="Alt+K", triggered=self.check_win)

    def check_win(self):
        if self.isHidden(): 
            self.show()
        else: 
            self.hide()

    def set_input_focus(self):
        self.input_frame.setFocus()
        self.input.setFocus()

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)

        self.trayIconMenu.addAction(self.hideAction)
        self.trayIconMenu.addAction(self.quitAction)
        # self.trayIconMenu.addAction(self.showAction)

        self.trayIcon = QSystemTrayIcon(_pkg.icon_path("logo.png", True))
        self.trayIcon.setContextMenu(self.trayIconMenu)

        self.trayIcon.activated.connect(self.check_win)

    def showMessage(self, title: str, body: str, icon: int=1, limit: int=5):
        tray = QSystemTrayIcon(_pkg.icon_path("logo.png", True))
        icon_ = tray.MessageIcon(icon)
        
        tray.showMessage(title, body, icon_, limit * 2000)
        tray.show()

    # def command_manager(self) -> None:
    #     text = self.input.text().strip().split(maxsplit=3)
        
    #     # ext_func = {
    #     #     "run": self.run_plugin,
    #     #     "install": ...,
    #     #     "remove": ...,
    #     #     "delete": ...,
    #     #     "show": ...,
    #     #     "update": ...,
    #     #     "open": ...}

    #     mkw = text[0].strip()
    #     kw = text[1].strip()
    #     arg = text[2].strip()
    #     value = text[3].strip()

    #     if mkw in (">", ">>"):
    #         if kw in ("ext", "extension"):
    #             if arg in ("run", "start"):
    #                 self.reset_input()
    #                 self.input.addAction(self.ClearSessionAction)
                                        
    #                 self.set_plugin(set_text=value)
    #                 self.search_plugin(set_text=value)

    #         elif kw in ("set", "var"):
    #             import re
    #             patt = re.compile(r"\s*(cmd|math|py)\(\s*(\w*\W*\S*)\s*\)\s*")
    #             find = patt.findall(value)
    #             print(find)

    #             self.global_vars.update({arg: value.lstrip("=").strip()})


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.setQuitOnLastWindowClosed(False)
    exit(app.exec_())

if __name__ == "__main__":
    main()
