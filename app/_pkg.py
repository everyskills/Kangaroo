#!/usr/bin/python3

import os
import json
import subprocess
import vlc
import sys

from threading import Thread
from glob import glob
from PyQt5.QtCore import QFileInfo, QSize, Qt, QRect
from PyQt5.QtGui import QFont, QImage, QIcon, QBrush, QPixmap, QPainter, QWindow
from PyQt5.QtWidgets import QFileIconProvider, QListWidgetItem

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## return os.path
def icon_path(_file: str, icon: bool=False):
    if icon: 
        return QIcon(base_dir + "icons/" + _file)
    else:
        return base_dir + "icons/" + _file

def ui_path(_file: str):
    return base_dir + "ui/" + _file

def style_path(_file: str):
    return base_dir + "styles/" + _file

# function to alter image
def mask_image(imgdata, img_size: tuple=(100, 100), size: int=64):

    imgtype = os.path.splitext(os.path.split(imgdata)[1])[1]

    # Load image
    image = QImage.fromData(open(imgdata, "rb").read(), imgtype)

    # convert image to 32-bit ARGB (adds an alpha
    # channel ie transparency factor):
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) // 2,
        (image.height() - imgsize) // 2,
        imgsize,
        imgsize)

    image = image.copy(rect)

    # Create the output image with the same dimensions
    # and an alpha channel and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle
    # with the original image onto the output image:
    brush = QBrush(image)

    # Paint the output image
    painter = QPainter(out_img)
    painter.setBrush(brush)

    # Don't draw an outline
    painter.setPen(Qt.NoPen)

    # drawing circle
    painter.drawEllipse(0, 0, imgsize, imgsize)

    # closing painter event
    painter.end()

    # Convert the image to a pixmap and rescale it.
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(img_size[0], img_size[1], Qt.KeepAspectRatio,
                   Qt.SmoothTransformation)

    # return back the pixmap data
    return pm

def add_item(obj, icon: str="", text: str="", tooltip: str="",
            selectable: bool=False, select: bool=False, checkable: bool=False, 
            check: bool=False, hide: bool=False, font_size: int=12, icon_size=(25, 25)):

    font = QFont()
    font.setPointSize(font_size)
    
    att = QListWidgetItem()
    att.setText(text)
    att.setHidden(hide)
    att.setFont(font)

    if icon: 
        att.setIcon(icon)
    if tooltip: 
        att.setToolTip(tooltip)
    if checkable:
        att.setCheckState(check)
    if selectable:
        att.setSelected(select)

    obj.setIconSize(QSize(icon_size[0], icon_size[1]))

    return att

def get_line(obj):
    text = str(obj.text()).strip()
    try:
        ext = text.split(":")
        suffix = ""

        for i in ext[1:]:
            suffix += " " + i

        if len(ext) >= 2:
            return ext[0], suffix.strip()
    
    except IndexError:
        return None

def icon_types(_file, icon: bool =False):
    file_type = os.path.splitext(os.path.split(_file)[1])[1].strip(".")
    ## set image/video icon
    if file_type in json.load(open(base_dir + "api/icons.json")).get("image"):
        return QIcon(_file)

    ## Default System Icons
    else:
        fileInfo = QFileInfo(_file)
        iconProvider = QFileIconProvider()
        icon = iconProvider.icon(fileInfo)
        return icon

def api_icons(_type: str):
    try:
        return json.load(open(base_dir + "api/icons.json")).get(_type)
    except KeyError:
        return ""

def Import(_file: str):
    import importlib 
    spec = importlib.util.spec_from_file_location(_file, _file)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

def set_image(_file: str, icon: bool=False, size: int=150):
    if icon:
        return _file.pixmap(QSize(size, size))
    else:
        return QIcon(_file).pixmap(QSize(size, size))

def add_item_widget(obj, item_widget, icon: str="", text: str="", 
                desc: str="", hotkey: str="", icon_size=30,
                no_desc: bool=False):

    frame = item_widget()

    # frame.image.setPixmap(set_image(icon, size=icon_size))
    frame.title.setText(text)
    frame.shortcut.setText(hotkey)
    
    if no_desc:
        frame.desc.hide()
        frame.desc.setStyleSheet("")
    else:
        frame.desc.show()
        frame.desc.setText(desc)

    item_list = add_item(obj, icon)
    item_list.setSizeHint(QSize(250, 40))

    return (item_list, frame)

def get_sys_icon(_name: str):
    return QIcon.fromTheme(_name)

def _ext_json(_path: str, key: str, value: str=""):
    return json.load(open(str(_path + "package.json"))).get(key.lower(), value)

def _get_path_ext_json(query: str, key: str="", value: str=""):
    for i in glob(base_dir + "exts/pu.*.ext/"):
        if _ext_json(i, "key_word") == query:
            return _ext_json(i, key, value), i

def set_item_widget(obj, item):
    obj.addItem(item[0])
    obj.setItemWidget(item[0], item[1])

def set_item(obj, item):
    obj.addItem(item)

def run_app(cmd):
    thread = Thread(target=subprocess.call,
                    kwargs={"shell": True, "args": cmd})
    thread.start()

class video_player:
    def __init__(self, frame, file: str="", on_changed: object=None):
        self.frame = frame
        self.file = file
        self.on_changed = on_changed

        self.__instance = vlc.Instance()
        self.__mediaplayer = self.__instance.media_player_new()

        if self.on_changed:
            self.__vlc_event_manager = self.__mediaplayer.event_manager()
            self.__vlc_event_manager.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.on_changed)

        if sys.platform.startswith("linux"):
            self.__mediaplayer.set_xwindow(self.frame.winId())
        
        elif sys.platform == "win32":
            self.__mediaplayer.set_hwnd(self.frame.winId())
        
        elif sys.platform == "darwin":
            self.__mediaplayer.set_nsobject(self.frame.winId())

        if self.file: 
            media = self.__instance.media_new(self.file)
            self.__mediaplayer.set_media(media)

    @property
    def media(self):
        return self.__mediaplayer
    
    @property
    def instance(self):
        return self.__instance
    
    def set_media(self, file):
        media = self.__instance.media_new(file)
        self.__mediaplayer.set_media(media)
