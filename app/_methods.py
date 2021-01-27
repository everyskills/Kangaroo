#!/usr/bin/python3

import re

class Controls:
    def __init__(self, parent=None) -> None:
        self.__parent = parent

    def close_win(self):
        self.__parent.close()

    def hide_win(self):
        self.__parent.hide()

    def show_win(self):
        self.__parent.show()

    def set_win_height(self, h: int):
        if not h < 70:
            self.__parent.setFixedHeight(h)
        
    def set_win_width(self, w: int):
        if not w > 700:
            self.__parent.setFixedWidth(w)

    def set_win_size(self, w: int, h: int):
        self.__parent.setFixedSize(w, h)

    def set_small_mode(self):
        self.__parent.def_setup.small_size()
    
    def set_extend_mode(self):
        self.__parent.def_setup.larg_size()

    def get_input(self, text: str):
        patt = re.compile(r"\$\(([a-z-A-Z_0-9]+)\)")
        find = patt.findall(self.__parent.input.text().strip())

        for i in find:
            text = patt.sub(self.__parent.global_vars.get(i.strip(), ""), self.__parent.input.text().strip())
        return text
        # for k, v in self.__parent.global_vars.items():
        #     text = text.replace("$(" + k + ")", v)
        # return text
