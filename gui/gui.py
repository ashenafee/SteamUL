# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import sys
import webbrowser

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget

from classes.steamunlocked import SteamUL
from cli.download import save_file
from cli.download import unzip_dl


class MainMenuUI(object):

    def __init__(self):
        self.layoutWidget = None
        self.searchL = None
        self.searchLayout = None
        self.searchInput = None
        self.searchButton = None
        self.sulTitle = None
        self.horizontalLayoutWidget = None
        self.resultsL = None
        self.resultsF = None
        self.verticalLayoutWidget = None
        self.verticalLayoutWidget_2 = None
        self.infoL = None
        self.buttonsL = None

    def setup_ui(self, mainmenu):
        mainmenu.setObjectName("mainmenu")
        mainmenu.setWindowModality(QtCore.Qt.NonModal)
        mainmenu.resize(500, 500)
        mainmenu.setFixedSize(500, 500)
        mainmenu.setAutoFillBackground(True)
        self.layoutWidget = QtWidgets.QWidget(mainmenu)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 462, 254))
        self.layoutWidget.setObjectName("layoutWidget")
        self.searchL = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.searchL.setContentsMargins(0, 0, 0, 0)
        self.searchL.setObjectName("searchL")
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        self.searchInput = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.searchInput.setFont(font)
        self.searchInput.setObjectName("searchInput")
        self.searchLayout.addWidget(self.searchInput)
        self.searchButton = QtWidgets.QPushButton(self.layoutWidget)
        self.searchButton.setMinimumSize(QtCore.QSize(0, 0))
        self.searchButton.setMaximumSize(QtCore.QSize(73, 25))
        self.searchButton.setFlat(False)
        self.searchButton.setObjectName("searchButton")
        self.searchLayout.addWidget(self.searchButton, 0,
                                    QtCore.Qt.AlignHCenter |
                                    QtCore.Qt.AlignVCenter)
        self.searchL.addLayout(self.searchLayout)
        self.sulTitle = QClickableImage(self.layoutWidget,
                                        "https://github.com/ashenafee/SteamUL")
        font = QtGui.QFont()
        font.setPointSize(64)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sulTitle.setFont(font)
        self.sulTitle.setText("")

        cover = QtGui.QImage()
        cover.loadFromData(
            requests.get("https://i.imgur.com/i2i5cbp.png").content)

        self.sulTitle.setPixmap(QtGui.QPixmap(cover))
        self.sulTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.sulTitle.setObjectName("sulTitle")
        self.searchL.addWidget(self.sulTitle)
        self.horizontalLayoutWidget = QtWidgets.QWidget(mainmenu)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 270, 461, 221))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.resultsL = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.resultsL.setContentsMargins(0, 0, 0, 0)
        self.resultsL.setObjectName("resultsL")
        self.resultsF = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.resultsF.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.resultsF.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resultsF.setObjectName("resultsF")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.resultsF)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 231, 219))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.infoL = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.infoL.setContentsMargins(0, 0, 0, 0)
        self.infoL.setObjectName("infoL")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.resultsF)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 0, 231, 219))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.buttonsL = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.buttonsL.setContentsMargins(0, 0, 0, 0)
        self.buttonsL.setObjectName("buttonsL")
        self.resultsL.addWidget(self.resultsF)

        self.retranslate_ui(mainmenu)
        QtCore.QMetaObject.connectSlotsByName(mainmenu)

    def retranslate_ui(self, mainmenu):
        _translate = QtCore.QCoreApplication.translate
        mainmenu.setWindowTitle(_translate("MainMenu", "SteamUL"))
        self.searchInput.setPlaceholderText(_translate("MainMenu", "Search "
                                                                   "for your "
                                                                   "game "
                                                                   "here..."))
        self.searchButton.setText(_translate("MainMenu", "Search"))


class GetThread(QThread):
    finished = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(object)

    def __init__(self, num=None, steam=None):
        QThread.__init__(self)
        self.num = num
        self.steam = steam
        self.dl_items = None

    def get_dl(self):
        try:
            dl = self.steam.results[self.num]['download']
            dl_name = self.steam.results[self.num]['dl_name']
            self.result.emit((dl, dl_name))
        except KeyError:
            self.dl_items = self.steam.download_link(self.num)
            self.result.emit(self.dl_items)

    def run(self):
        self.get_dl()
        self.finished.emit()


class DownloadThread(QThread):
    data = QtCore.pyqtSignal(object)

    def __init__(self, num=None, steam=None):
        QThread.__init__(self)
        self.num = num
        self.steam = steam

    def run(self):
        self.data.emit('Finding path...')
        name = self.steam.results[self.num]['name']
        name = f"{name.replace(':', '-').replace('?', '-')}.zip"
        file_path = os.path.join(".", name)

        self.data.emit('Downloading (please wait)...')
        zip_path = save_file(self.steam.results[self.num]['download'],
                             file_path)

        self.data.emit('Unzipping (please wait)...')
        unzip_dl(self.steam.results[self.num]['name'], zip_path)

        self.data.emit('Done!')


class QDownloadButton(QPushButton):
    def __init__(self, parent, num=None, steam=None, mainmenu=None):
        QPushButton.__init__(self, parent)
        self.num = num
        self.steam = steam
        self.ddl_tuple = None
        self.ddl = None
        self.ddl_name = None
        self.ddl_size = None

        self.mainmenu = mainmenu

        self.thread = None
        self.thread1 = None

    def mousePressEvent(self, event):
        self.mainmenu.grab_ddl(self)


class QYesButton(QPushButton):
    def __init__(self, parent, num=None, steam=None, mainmenu=None):
        QPushButton.__init__(self, parent)
        self.num = num
        self.steam = steam
        self.mainmenu = mainmenu


class QCancelButton(QPushButton):
    def __init__(self, parent, mainmenu=None):
        QPushButton.__init__(self, parent)
        self.mainmenu = mainmenu

    def go_back(self):
        # Reveal results
        self.mainmenu.restore_results()


class QClickableLabel(QLabel):
    def __init__(self, parent, num=None, steam=None, mainmenu=None):
        QLabel.__init__(self, parent)
        self.num = num
        self.steam = steam
        self.info = None
        self.mainmenu = mainmenu
        self.resultsVL = None

    def mousePressEvent(self, event):
        if self.steam is not None:
            self.mainmenu.grab_info(self)
            self.mainmenu.resultsL.setAlignment(self.mainmenu.original_align)

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet("color: red")
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet("color: black")


class QClickableImage(QLabel):
    def __init__(self, parent, link=None):
        QLabel.__init__(self, parent)
        self.link = link

    def mousePressEvent(self, event):
        if self.link is not None:
            webbrowser.open(self.link)

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet(
            "border-style: outset; border-width: 2px; border-color: black")
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet("")


class MainMenu(QWidget, MainMenuUI):

    def __init__(self):
        QWidget.__init__(self)
        self.setup_ui(self)
        self.game_query = None
        self.choice = None

        self.steam = None
        self.num = None

        self.info_label = None

        self.ddl_tuple = None
        self.ddl = None
        self.ddl_name = None
        self.ddl_size = None
        self.info = None
        self.ddl_clicked = None

        self.qyesbutton = None
        self.no_btn = None
        self.dl_option_buttons = []
        self.file_path = None

        self.thread = None
        self.thread1 = None
        self.thread2 = None
        self.thread3 = None
        self.dlthread = None

        self.original_align = None
        self.resultsVL = QtWidgets.QVBoxLayout()
        self.resultsVL.setObjectName("resultsVL")
        self.resultsF1 = QtWidgets.QFrame()
        self.resultsF1.setLayout(self.resultsVL)

        self.searchButton.clicked.connect(self.search_button)

    def search_button(self):

        try:
            if self.children()[1].children()[2].children()[0].count() > 0:
                self.clear_results()
        except IndexError:
            pass
        except AttributeError:
            pass

        if self.searchInput.text() != '':
            self.game_query = self.searchInput.text()

            # Create SteamUL object
            self.steam = SteamUL(self.game_query)

            # Get results
            self.steam.search_results()

            # Update results
            if self.steam.results != {}:

                # Add vertical layout to the left of choice selection
                self.resultsVL.setContentsMargins(0, 0, 0, 0)
                self.resultsVL.setSpacing(0)
                self.resultsL.insertWidget(0, self.resultsF1)
                if self.original_align is None:
                    self.original_align = self.resultsL.alignment()
                self.resultsL.setAlignment(QtCore.Qt.AlignTop)

                # Create each result QLabel item to be placed in <resultsVL>
                i = 1
                for item in self.steam.results:
                    result_text = f"[{i}] {self.steam.results[item]['name']}\n"
                    result_label = QClickableLabel(result_text, i, self.steam,
                                                   self)

                    # Format <result_label>
                    result_label.setFont(QFont('MS Shell Dlg 2', 12))
                    result_label.setFixedHeight(40)

                    self.resultsVL.addWidget(result_label)
                    i += 1

    def grab_info(self, clicked):
        # Grab the Steam info for the selected game
        self.num = clicked.num
        self.info = self.steam.steam_info(self.num)

        # Clear search results
        self.clear_all_results()

        # Change cover image displayed
        cover_img = self.sulTitle
        image = QtGui.QImage()
        image.loadFromData(requests.get(self.info['img']).content)
        cover_img.setPixmap(QtGui.QPixmap(image))
        cover_img.link = self.info['link']

        # Update text information shown
        desc_label = QLabel(self.info['desc'])
        desc_label.setWordWrap(True)
        desc_label.setFixedWidth(200)

        rev_label = QLabel(f"All reviews:\t{self.info['reviews']}")
        rel_label = QLabel(f"Release:\t\t{self.info['release']}")
        dev_label = QLabel(f"Developer(s):\t{self.info['dev']}")
        pub_label = QLabel(f"Publisher(s):\t{self.info['pub']}")

        info_layout = self.children()[1] \
            .children()[1] \
            .children()[0] \
            .children()[0]

        info_layout.addWidget(desc_label)
        info_layout.addWidget(rev_label)
        info_layout.addWidget(rel_label)
        info_layout.addWidget(dev_label)
        info_layout.addWidget(pub_label)

        # Add buttons
        download_btn = QDownloadButton("Download", self.num, self.steam, self)
        download_btn.setFixedHeight(105)
        cancel_btn = QCancelButton("Cancel", self)
        cancel_btn.setFixedHeight(105)
        cancel_btn.clicked.connect(cancel_btn.go_back)

        buttons_layout = \
            self.children()[1].children()[1].children()[1].children()[0]

        buttons_layout.addWidget(download_btn)
        buttons_layout.addWidget(cancel_btn)

    def grab_ddl(self, clicked):
        # Grab download
        self.ddl_clicked = clicked
        self.thread = GetThread(self.num, self.steam)
        self.thread.result.connect(self.ddl_return)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        self.wait_delay()

    def wait_delay(self):
        buttons_layout = \
            self.children()[1].children()[1].children()[1].children()[0]

        # Clear the "Download" and "Cancel" button in <buttonsL>
        for i in reversed(range(buttons_layout.count())):
            self.dl_option_buttons.append(buttons_layout.itemAt(i).widget())
            buttons_layout.itemAt(i).widget().setParent(None)

        # Add confirmation text
        conf_label = QLabel(f"Waiting for UploadHaven's delay...")
        buttons_layout.addWidget(conf_label)

    def ddl_return(self, ddl_tuple):
        self.ddl_tuple = ddl_tuple
        self.ddl = self.ddl_tuple[0]
        self.ddl_name = \
            self.ddl_tuple[1][:self.ddl_tuple[1].index("Size:")].strip()
        self.ddl_size = self.ddl_tuple[1][self.ddl_tuple[1].index("Size:"):]
        self.add_yes_no_download()

    def add_yes_no_download(self):
        # Update GUI
        buttons_layout = \
            self.children()[1].children()[1].children()[1].children()[0]

        # Clear the "Download" and "Cancel" button in <buttonsL>
        for i in reversed(range(buttons_layout.count())):
            buttons_layout.itemAt(i).widget().setParent(None)

        # Add confirmation text
        conf_label = QLabel(
            f"Click 'Yes' to download:\n{self.ddl_name}\n{self.ddl_size}")

        # Add "Yes" and "No" buttons
        self.qyesbutton = QYesButton("Yes", self.num, self.steam)
        self.qyesbutton.clicked.connect(self.download)
        self.qyesbutton.setObjectName("yesBtn")
        self.no_btn = QPushButton("No")
        self.no_btn.clicked.connect(self.no_download)
        self.no_btn.setObjectName("noBtn")

        buttons_layout.addWidget(conf_label)
        buttons_layout.addWidget(self.qyesbutton)
        buttons_layout.addWidget(self.no_btn)

    def download(self):
        # Remove Yes/No buttons
        curr_layout = self.qyesbutton.parent().children()[0]
        for i in reversed(range(curr_layout.count())):
            if type(curr_layout.itemAt(i).widget()) is not QLabel:
                curr_layout.itemAt(i).widget().setParent(None)

        # Get label to show status of download
        self.info_label = curr_layout.parent().children()[1]
        self.info_label.setText("")

        self.dlthread = DownloadThread(self.num, self.steam)
        self.dlthread.data.connect(self.data_ready)
        self.dlthread.start()

    def no_download(self):
        # Update GUI
        buttons_layout = \
            self.children()[1].children()[1].children()[1].children()[0]

        # Clear the "Download" and "Cancel" button in <buttonsL>
        for i in reversed(range(buttons_layout.count())):
            buttons_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(len(self.dl_option_buttons))):
            if buttons_layout.count() < 2:
                buttons_layout.addWidget(self.dl_option_buttons[i])

    def data_ready(self, data):
        self.info_label.setText(f"{self.info_label.text()}\n{data}")

    def make_path(self):
        name = self.steam.results[self.num]['name']
        name = f"{name.replace(':', '-').replace('?', '-')}.zip"
        self.file_path = os.path.join("./SteamUL Downloads", name)

    def save(self):
        save_file(self.steam.results[self.num]['download'], self.file_path)

    def clear_results(self):
        """Check if there are already search results present."""
        old_results = self.children()[1].children()[2].children()[0]
        for i in reversed(range(old_results.count())):
            old_results.itemAt(i).widget().setParent(None)

    def clear_all_results(self):
        info_l = self.resultsF.children()[0].children()[0]
        buttons_l = self.resultsF.children()[1].children()[0]

        # Clear info labels
        if info_l.count() > 0:
            for i in reversed(range(info_l.count())):
                info_l.itemAt(i).widget().setParent(None)

        # Clear buttons
        for i in reversed(range(buttons_l.count())):
            buttons_l.itemAt(i).widget().setParent(None)

        self.resultsF1.hide()

    def restore_results(self):
        info_l = self.children()[1].children()[1].children()[0]
        for item in info_l.children():
            if type(item) is QtWidgets.QLabel:
                item.setParent(None)
        cover = QtGui.QImage()
        cover.loadFromData(
            requests.get("https://i.imgur.com/i2i5cbp.png").content)
        self.sulTitle.setPixmap(QtGui.QPixmap(cover))
        self.sulTitle.link = "https://github.com/ashenafee/SteamUL"
        self.resultsL.setAlignment(QtCore.Qt.AlignTop)
        self.resultsF1.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainMenu()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
