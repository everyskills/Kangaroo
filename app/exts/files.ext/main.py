#!/usr/bin/python3

import os

from glob import glob
from humanize import naturalsize
from PyQt5.QtGui import QDesktopServices, QIcon, QMovie
from PyQt5.QtCore import QFileInfo, QUrl, QSize
from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.uic import loadUi

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Plugin(QWidget):
    def __init__(self, line_edit, pkg, parent):
        super(Plugin, self).__init__()
        QWidget.__init__(self)

        self.input = line_edit
        self.pkg = pkg
        self.parent = parent
        self.undo = ""

        self.ui = loadUi(base_dir + "files.ui", self)

        # self.input.textChanged.connect(lambda: self.query_file())
        self.input.textChanged.connect(lambda: self.query_file())
        self.ui.list_widget.itemClicked.connect(self.add_click_path)
        self.ui.list_widget.itemSelectionChanged.connect(self.get_path_info)
        self.ui.btn_video.clicked.connect(self.start_video)
        self.ui.slide_video.sliderMoved.connect(self.set_video_pos)

        enterAction = QAction("enter", self, shortcut="Return", triggered=self.get_enter_item)
        self.ui.list_widget.addAction(enterAction)
        
        undoAction = QAction("undo", self, shortcut="Alt+Left", triggered=self.remove_suffix_dir)
        self.input.addAction(undoAction)

        nextAction = QAction("next", self, shortcut="Alt+Right", triggered=self.return_suffix_dir)
        self.input.addAction(nextAction)
        
        self.video_player = self.pkg.video_player(self.ui.image, "", self.media_time_changed)
        self.query = str(self.input.text()).strip()
        # self.query = self.parent.get_input(self.input.text().strip())

        _icon = self.pkg.icon_types(self.query)
        self.ui.image.setPixmap(self.pkg.set_image(_icon, icon=True, size=150))

        self.short_title(os.path.split(self.query)[1])
        
        self.query_file()
        self.start_up()

    def remove_suffix_dir(self):
        suffix = os.path.split(os.path.abspath(self.input.text().strip()))
        self.undo = "/" + suffix[1]
        self.input.setText(str(suffix[0]))

    def return_suffix_dir(self):
        self.input.insert(self.undo)
        self.undo = ""

    def get_enter_item(self):
        self.add_click_path(self.ui.list_widget.currentItem())
        self.ui.list_widget.setFocus()

    def start_up(self):
        self.ui.slide_video.hide()
        self.ui.label_slide_value.hide()
        self.ui.btn_video.hide()

    def query_file(self):
        self.ui.list_widget.clear()
        self.query = self.input.text().strip()
        # self.query = self.parent.get_input(self.input.text().strip())

        _path, _file_count, _folder_count, _size = None, 0, 0, 0.00

        if len(self.query) == 1 and self.query.startswith("~"):
            self.input.insert("/")

        if self.query.startswith(("/", "~")):
            _path = os.path.expanduser(self.query)

        # elif self.query.startswith("$"):
        elif "$" in self.query:
            _path = os.path.expandvars(self.query)

        if _path:
            all_path = glob(_path + "*")
            for i in all_path:
                if not os.path.isfile(i):
                    _icon = self.pkg.icon_types(i)
                    _folder_count += 1
                    _size += os.path.getsize(i)

                elif not os.path.isdir(i):
                    _icon = self.pkg.icon_types(i)
                    _file_count += 1
                    _size += os.path.getsize(i)

                else:
                    _icon = self.pkg.icon_types(i)
                    _file_count += 1
                    _size += os.path.getsize(i)
                
                frame = self.pkg.Import(base_dir + "item.py").Ui_Item
                item = self.pkg.add_item_widget(self.ui.list_widget, frame, _icon, str(os.path.split(i)[1]), i, icon_size=25)
                self.pkg.set_item_widget(self.ui.list_widget, item)
                self.ui.status.setText(f"{_folder_count} {'Folder' if _folder_count <= 1 else 'Folders'}, {_file_count} {'File' if _file_count <= 1 else 'Files'} ({naturalsize(_size, True, format='%.1f ')})")

    def hide_video(self):
        if self.video_player.media.is_playing():
            self.video_player.media.stop()
        
        self.ui.btn_video.hide()
        self.ui.slide_video.hide()
        self.ui.label_slide_value.clear()
        self.ui.slide_video.hide()

    def show_video(self):
        self.ui.btn_video.setIcon(QIcon(base_dir + "icons/play.png"))
        self.ui.slide_video.setValue(0)
        self.ui.btn_video.show()
        self.ui.slide_video.show()
        self.ui.label_slide_value.show()

    def get_path_info(self):
        item = self.ui.list_widget.currentItem()
        litem = item.listWidget().itemWidget(item)

        _file = litem.title.text()
        _path = litem.desc.text()

        self.short_title(_file)
        self.set_data(_path)

        try:
            img = tuple(self.pkg.api_icons("image"))
            video = tuple(self.pkg.api_icons("video"))
            audio = tuple(self.pkg.api_icons("audio"))
        except TypeError:
            img = ".jpg"
            video = ".mp4"
            audio = ".mp3"

        if _file.endswith(".gif"):
            self.hide_video()
            movie = QMovie(_path)
            movie.setScaledSize(QSize(300, 200))
            self.ui.image.setMovie(movie)
            movie.start()
       
        elif _file.endswith(img):
            self.hide_video()
            self.ui.image.setPixmap(self.pkg.set_image(item.icon(), size=300))
       
        elif _file.endswith(video) or _file.endswith(audio):
            self.ui.image.setPixmap(self.pkg.set_image(item.icon(), size=150))
            self.video_player.set_media(_path)
            self.show_video()

        else:
            self.hide_video()
            self.ui.image.setPixmap(self.pkg.set_image(item.icon(), size=150))
            
    def set_data(self, _file):
        ff = QFileInfo(_file)
        self.short_title(ff.fileName())
        self.ui.lsize.setText(naturalsize(ff.size(), format="%.1f "))

        if ff.isDir():
            self.ui.litems.show()
            self.ui.label_3.show()
            self.ui.litems.setText(str(len(glob(_file + "/*"))))
        else:
            self.ui.label_3.hide()
            self.ui.litems.hide()

        self.ui.lcreated.setText(ff.created().toString())
        self.ui.lmodified.setText(ff.lastModified().toString())
        self.ui.laccessed.setText(ff.lastRead().toString())
        self.ui.luser.setText(ff.owner())
        self.ui.luid.setText(str(ff.ownerId()))
        self.ui.lgroup.setText(str(ff.group()))
        self.ui.lgid.setText(str(ff.groupId()))
        self.ui.lpath.setText(ff.path())
        # self.lpermissions.setText(str(ff.permissions())

    def add_click_path(self, item):
        item = item.listWidget().itemWidget(item)
        _path = item.desc.text()

        self.set_data(_path)

        if not os.path.isfile(_path):
            wh = "" if not os.path.isdir(os.path.expanduser(_path)) else "/"
            self.input.setText(_path + wh)
        else:
            QDesktopServices().openUrl(QUrl(_path)) # from PyQt5
            self.parent.hide_win()
            # self.run_app(f"xdg-open '{_path}'") # from CLI
            # self.close()

    def short_title(self, item: str):
        if len(item) <= 20:
            self.ui.title.setText(item)
        else:
            self.ui.title.setText(item[0:21] + "...")

    def start_video(self):
        if self.video_player.media.is_playing():
            self.video_player.media.pause()
            self.ui.btn_video.setIcon(QIcon(base_dir + "icons/play.png"))
        else:
            self.video_player.media.play()
            self.ui.btn_video.setIcon(QIcon(base_dir + "icons/pause.png"))

    def set_video_pos(self):
        pos = self.ui.slide_video.value()
        self.video_player.media.set_position(pos / 100)

    def media_time_changed(self, event):
        pos = self.video_player.media.get_position() * 100
        self.ui.slide_video.setValue(int(pos))        
        self.ui.label_slide_value.setText(str(int(pos)) + "%")

        if int(pos) >= 100 or int(pos) >= 99:
        	self.ui.slide_video.clear()
        	self.video_player.media.set_position(0.00)
        	self.ui.slide_video.setValue(0)
        	self.video_player.media.pause()
