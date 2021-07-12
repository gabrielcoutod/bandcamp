# Bandcamp
Scripts for searching, downloading and playing bandcamp albums.

# Dependencies
To install python dependencies: 
```
pip install -e .
```
You also need ffmpeg:
```
sudo apt install ffmpeg
```
# How to use
To search albums on bandcamp (-a flag searches all pages):
```
 python3 bandcamp/bandcamp.py search <LINK> [-a]
```

To download albums from bandcamp (as mp3 with metadata):
```
 python3 bandcamp/bandcamp.py download <LINK> <DOWNLOAD DIR>
```

To play albums from bandcamp (downloads and plays them):
```
 python3 bandcamp/bandcamp.py play <LINK>
```
