import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import func
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
            output_path=path, filename=self.title
        )

    def save(self, path):
        stream = self.get_stream()
        t = Thread(target=self.pull, args=(stream, path,))
        t.start()

    def __str__(self):
        return f"Title:{self.title}\nThumbnail:{self.thumbnail}"



class Results:
    NUM_RESULTS = 10

    def __init__(self, query):
        self.query = query
        self.page = BeautifulSoup(requests.get("https://www.youtube.com/results?search_query=" + query).text, 'lxml')
        self.vids = self.page.findAll('a', attrs={'class': 'yt-uix-tile-link'})[0:__class__.NUM_RESULTS]
        self.thumbnails = self.page.findAll(
            'a',
            attrs={'id': 'item-section-854530'}
        )[0:__class__.NUM_RESULTS]
        self.songs = []
        self.images = []
        print(self.thumbnails)
        for i in range(0, __class__.NUM_RESULTS-1):
            print(re.findall('src="(.*?)"', str(self.thumbnails[i])))
            self.songs.append(Song(self.vids[i], re.findall('src="(.*?)"', str(self.thumbnails[i]))[0]))

    def get(self):
        return self.songs



