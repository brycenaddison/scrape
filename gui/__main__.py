from gui.window import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide2 import QtGui
from PySide2.QtCore import QTimer
from download import func
from download.data import Song, Results
from threading import Thread
import requests
import urllib.request
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.showing_song = False
        self.text_layout()

        self.song = None
        self.downloads = []
        self.download_in_progress = False

        self.search_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.progress_bar.hide()
        self.download_path = func.get_download_path()
        self.download_dir.setText(self.download_path)

        self.dir_button.clicked.connect(self.change_dir)
        self.search_button.clicked.connect(self.search)
        self.search_bar.textChanged.connect(self.check_field)
        self.download_button.clicked.connect(self.download_song)

        self.timer = QTimer()
        self.timer.setInterval(15)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.run_search)

        self.text("Search for song...")
        self.progress_label.setText("No downloads in progress.")

    @staticmethod
    def red(text):
        return f"<html><head/><body><p><span style=\" font-weight:600; color:#ff0206;\">{text}</span></p></body></html>"

    def check_field(self):
        if self.search_bar.text().strip(" ") == "":
            self.search_button.setEnabled(False)
        else:
            self.search_button.setEnabled(True)

    def search(self):
        self.download_button.setEnabled(False)
        self.song = None
        self.text("Searching...")
        self.timer.start()

    def run_search(self):
        try:
            results = Results(self.search_bar.text().strip(" ")).get()
            if len(results) == 0:
                self.text(__class__.red("No results found. Try a different query."))
            else:
                self.change_song(results[0])
        except requests.exceptions.ConnectionError:
            self.text(__class__.red("Connection error encountered. Connect to the internet and try again."))

    def change_dir(self):
        self.download_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.download_dir.setText(QApplication.translate("MainWindow", self.download_path, None, -1))

    def change_song(self, song: Song):
        self.song = song
        data = urllib.request.urlopen(song.get_thumbnail()).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.picture_label.setPixmap(QtGui.QPixmap(image))
        self.song_name_label.setText(QApplication.translate("MainWindow", song.get_title(), None, -1))
        self.download_button.setEnabled(True)
        if not self.showing_song:
            self.song_layout()

    def download_song(self):
        self.downloads.append(self.song)
        if not self.download_in_progress:
            self.start_download()

    def start_download(self):
        for song in self.downloads:
            self.progress_label.setText(f"Downloading {song.get_title()}...")
            t = Thread(target=self.download_worker, args=(song,))
            t.start()

    def download_worker(self, song: Song):
        stream = song.get_stream()
        song.pull(stream, self.download_dir.text())
        self.text("Downloading")


    def progress_update(self):
        pass

    def text(self, text):
        self.info_text.setText(text)
        self.info_text.update()
        if self.showing_song:
            self.text_layout()

    def text_layout(self):
        self.change_search_button.hide()
        self.song_name_label.hide()
        self.picture_label.hide()
        self.info_text.show()
        self.showing_song = False

    def song_layout(self):
        self.info_text.hide()
        self.picture_label.show()
        self.song_name_label.show()
        self.change_search_button.show()
        self.showing_song = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
