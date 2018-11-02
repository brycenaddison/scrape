# Music-Scraper
Scrapes music from youtube using python and several libraries.
To use this download scraper.exe and place it in a folder that contains a music.txt file.
Within this music.txt put one song per line. Due to ads on YouTube some music will fail to download
To make the scraper more accurate put the artist as well as the title on the same line.
This works better because the scraper locates video links with a Youtube search query.
All music will be placed in a new Music subfolder also created by the program.

# Libraries in use
- Bueatiful Soup 4
  - lxml
- pytube
- requests
- os
