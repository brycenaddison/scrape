import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from download.func import ProgressBar
from threading import Thread
import time
import re


class Song:
    def __init__(self, vid, thumbnail):
        self.link = 'https://www.youtube.com' + vid['href']
        self.title = vid['title']
        self.thumbnail = thumbnail


    def get_stream(self):
        return YouTube(self.link)

    def pull(self, stream, path):
        stream.streams.filter(
            only_audio=True, file_extension='mp4'
        ).first().download(
            output_path=path, filename=self.title, file_extension='mp3'
        )

    def save(self, path):
        stream = self.get_stream()
        download = Thread(target=self.pull, args=(stream, path,))
        download.start()
        print(f"Downloading {self.title}...")
        progress_bar = ProgressBar()
        info = Thread(target=stream.register_on_progress_callback, args=(progress_bar.update,))
        start_time = ProgressBar.current_time()
        info.start()
        while not progress_bar.in_progress():
            time.sleep(0.05)
        while progress_bar.in_progress():
            progress_bar.print_progress(start_time)
            time.sleep(0.3)
        print(f"Finished downloading {self.title}.")

    def info(self):
        return f"Title:{self.title}\nThumbnail:{self.thumbnail}"

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def get_title(self):
        return self.title

    def get_thumbnail(self):
        return self.thumbnail


class Results:
    NUM_RESULTS = 10

    def __init__(self, query):
        self.query = query
        self.page = []
        self.vids = []
        self.thumbnails = []
        self.songs = []
        self.search_thread = Thread(target=self.run, args=(query,))
        self.search_thread.start()

    def run(self, query):
        self.page = BeautifulSoup(
            requests.get("https://www.youtube.com/results?search_query=" + query + "&sp=EgIQAQ%253D%253D").text, 'lxml')
        falsevids = self.page.findAll('a', attrs={'class': 'yt-uix-tile-link'})
        self.vids = self.page.findAll('a', attrs={'class': 'yt-uix-tile-link', 'aria-describedby': True})
        print(self.vids[0])
        self.thumbnails = self.page.findAll(
            'span',
            attrs={'class': 'yt-thumb-simple'}
        )

        while True:
            for i in range(len(self.vids)):
                if falsevids[i] != self.vids[i]:
                    del self.thumbnails[i]
                    break
            break


        print(self.thumbnails[0])
        for i in range(0, __class__.NUM_RESULTS):
            try:
                img = re.findall('data-thumb="(.*?)"', str(self.thumbnails[i]))[0].replace('&amp;', '&')
            except IndexError:
                try:
                    img = re.findall('src="(.*?)"', str(self.thumbnails[i]))[0].replace('&amp;', '&')
                except IndexError:
                    break
            if img.startswith("//"):
                img = "https:" + img
            self.songs.append(Song(self.vids[i], img))

    def thread_running(self):
        return self.search_thread.is_alive()

    def get(self):
        self.search_thread.join()
        return self.songs



