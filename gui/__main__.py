from gui.window import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow, QLabel, QPushButton
from PySide2 import QtGui, QtCore, QtWidgets
from download import func
from download.data import Song, Results
from multiprocessing.pool import ThreadPool
import urllib.request
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.text_display = False
        self.song = None
        self.ready = True
        self.search_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.download_path = func.get_download_path()
        self.download_dir.setText(QApplication.translate("MainWindow", self.download_path, None, -1))

        self.dir_button.clicked.connect(self.change_dir)
        self.search_button.clicked.connect(self.search)
        self.search_bar.textChanged.connect(self.check_field)
        self.info_text = None
        self.text("Search for song...")

    def red(self, text):
        return f"<html><head/><body><p><span style=\" font-weight:600; color:#ff0206;\">{text}</span></p></body></html>"

    def check_field(self):
        if self.search_bar.text().strip(" ") == "":
            self.search_button.setEnabled(False)
        else:
            self.search_button.setEnabled(True)

    def search(self):
        pool = ThreadPool(processes=1)
        pool.apply_async(
        results = Results(self.search_bar.text().strip(" ")).get()
        if len(results) == 0:
            self.text(self.red("No results found. Try a different query."))
        else:
            self.change_song(results[0])

    def change_dir(self):
        self.download_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.download_dir.setText(QApplication.translate("MainWindow", self.download_path, None, -1))

    def change_song(self, song: Song):
        if self.text_display:
            self.song_layout()
        self.song = song
        data = urllib.request.urlopen(song.get_thumbnail()).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.picture_label.setPixmap(QtGui.QPixmap(image))
        self.song_name_label.setText(QApplication.translate("MainWindow", song.get_title(), None, -1))

    def text_layout(self):
        self.change_search_button.deleteLater()
        self.song_name_label.deleteLater()
        self.picture_label.deleteLater()
        self.verticalLayout.deleteLater()
        self.horizontalLayout_5.deleteLater()
        self.info_text = QLabel(self.centralwidget)
        self.info_text.setTextFormat(QtCore.Qt.AutoText)
        self.info_text.setObjectName("info_text")
        self.search_layout.addWidget(self.info_text)
        self.text_display = True

    def text(self, text):
        if not self.text_display:
            self.text_layout()
        self.info_text.setText(QApplication.translate("MainWindow", text, None, -1))
        self.ready = True

    def song_layout(self):
        self.info_text.deleteLater()
        self.picture_label = QtWidgets.QLabel(self.centralwidget)
        self.picture_label.setText("")
        self.picture_label.setPixmap(QtGui.QPixmap("../../../Downloads/hqdefault.jpg"))
        self.picture_label.setObjectName("picture_label")
        self.song_box.addWidget(self.picture_label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.song_name_label = QtWidgets.QLabel(self.centralwidget)
        self.song_name_label.setObjectName("song_name_label")
        self.verticalLayout.addWidget(self.song_name_label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.change_search_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_search_button.setObjectName("change_search_button")
        self.horizontalLayout_5.addWidget(self.change_search_button)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.song_box.addLayout(self.verticalLayout)
        self.change_search_button.setText(QtWidgets.QApplication.translate("MainWindow", "Not correct?", None, -1))
        self.text_display = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
