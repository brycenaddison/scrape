from gui.window import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide2 import QtGui
from download import func
from download.data import Song, Results
import urllib.request
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.song = None

        self.search_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.download_path = func.get_download_path()
        self.download_dir.setText(QApplication.translate("MainWindow", self.download_path, None, -1))

        self.dir_button.clicked.connect(self.change_dir)
        self.search_button.clicked.connect(self.search)
        self.search_bar.textChanged.connect(self.check_field)

    def check_field(self):
        if self.search_bar.text().strip(" ") == "":
            self.search_button.setEnabled(False)
        else:
            self.search_button.setEnabled(True)

    def search(self):
        self.change_song(Results(self.search_bar.text().strip(" ")).get()[0])

    def change_dir(self):
        self.download_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.download_dir.setText(QApplication.translate("MainWindow", self.download_path, None, -1))

    def change_song(self, song: Song):
        self.song = song
        data = urllib.request.urlopen(song.get_thumbnail()).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.picture_label.setPixmap(QtGui.QPixmap(image))
        self.song_name_label.setText(QtWidgets.QApplication.translate("MainWindow", song.get_title(), None, -1))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
