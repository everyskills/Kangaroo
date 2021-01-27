#!/usr/bin/python3

import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QAction, QApplication

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

# Kangaroo

class MainWindowSettings:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        
    def init_setup(self):
        quitAction = QAction("E&xit", self.parent, shortcut="Ctrl+Q",
                             triggered=QApplication.instance().quit)
        
        closeeAction = QAction("Quit", self.parent, shortcut="Esc",
                                 triggered=self.parent.hide)
        
        focusAction = QAction("setFocus", self.parent, shortcut="F",
                             triggered=self.parent.input.setFocus)
        
        self.parent.input.addAction(focusAction)
        self.parent.addAction(closeeAction)
        self.parent.addAction(quitAction)

        self.parent.move(360, 100)
        self.parent.setFixedSize(650, 320)
        self.parent.setWindowFlags(self.parent.windowFlags() |
                            Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)

        QApplication.instance().setApplicationName("Kangaroo")
        QApplication.instance().setApplicationVersion("1.0.0")
        QApplication.instance().setQuitLockEnabled(True)
        
        # self.parent.setWindowIcon(QIcon(base_dir + "icons/logo.png"))

        self.parent.setWindowFlags(self.parent.windowFlags())

        self.parent.setWindowTitle("Kangaroo")
        
        self.parent.setStyleSheet(open(base_dir + "styles/default.qss").read())
        self.parent.btn_setting.setIcon(QIcon(base_dir + "icons/main/setting.svg"))
        self.parent.btn_ext.setIcon(QIcon(base_dir + "icons/main/search.svg"))

        self.parent.input.setFocus()

    def small_size(self):
        self.parent.setFixedHeight(70)
        self.parent.main_frame.hide()

    def larg_size(self):
        self.parent.setFixedHeight(600)
        self.parent.main_frame.show()

    def remove_session(self):
        self.parent.input.clear()
        self.parent.btn_ext.setText("")
        self.parent.input.setPlaceholderText("Search...")
        self.parent.btn_ext.setIcon(QIcon(base_dir + "icons/main/search.svg"))
        self.small_size()

    def input_setup(self):
        font = QFont()
        font.setPointSize(13)

        self.parent.input.setFont(font)
        self.parent.input.setMaxLength(999999999)
        self.parent.input.setFrame(False)
        self.parent.input.setCursorPosition(0)
        self.parent.input.setClearButtonEnabled(True)
        self.parent.input.setObjectName("input")
        
        focusAction = QAction("setFocus", self.parent, shortcut="F",
                             triggered=self.parent.input.setFocus)
        self.parent.input.addAction(focusAction)

