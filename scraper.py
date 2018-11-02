from bs4 import BeautifulSoup
from pytube import YouTube
import os
import requests
# Using lxml parser

# Load names of tracks
music = []
with open('music.txt', 'r') as f:
    for line in f:
        line = line[:-1]
        music.append(line)

# Get links for tracks on YouTube
links = []
vids = []
for track in music:
    base = "https://www.youtube.com/results?search_query="
    qstring = track
    r = requests.get(base + qstring)
    page = r.text
    soup = BeautifulSoup(page, 'lxml')
    vids.append(soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})[0])
for val in vids:
    tmp = 'https://www.youtube.com' + val['href']
    if(len(tmp) < 50):
        links.append(tmp)

# Creates new Music directory in the same folder to export files
path = os.getcwd()
newDir = path + '\\Music\\'

access_rights = 0o755

try:
    os.mkdir(newDir, access_rights)
except OSError:
    print("Creation of the Music directory %s failed" % newDir)
else:
    print("Successfully created the Music directory %s" % newDir)

# Downloads the songs to newDir Music
for link in links:
    yt = YouTube(link)
    yt.streams.filter(only_audio=True).first().download(newDir)

# Change all file types to mp3 from mp4
mp4List = os.listdir(newDir)

for i in range(len(mp4List)):
    os.rename(newDir + mp4List[i], newDir + mp4List[i][:-4] + '.mp3')
