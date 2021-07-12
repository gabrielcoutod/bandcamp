import requests
import bs4
import eyed3
import json
import argparse
from pathlib import Path
from pydub import AudioSegment
from io import BytesIO
from multiprocessing import Process


def download(link, album_dir, wav=False, metadata=True):
    album_dir = Path(album_dir)
    album_dir.mkdir(parents=True, exist_ok=True)

    # request for the page
    album_res = requests.get(link)
    # checks if no errors ocurred
    album_res.raise_for_status()

    # html parsing
    soup = bs4.BeautifulSoup(album_res.text, "html.parser")
    lst = soup.select("""script[type="application/ld+json"]""")
    album_text = lst[0].string.__str__()

    # album info
    album_info = json.loads(album_text)
    album_name = album_info["name"]
    album_artist = album_info["byArtist"]["name"]
    album_date = album_info["datePublished"]

    if metadata == True and wav == False:

        #downloads cover
        album_image_link = album_info["image"]
        image_res = requests.get(album_image_link)
        #checks for errors
        image_res.raise_for_status()

        # saves the album cover
        filename = "cover.jpg"
        filepath = album_dir / filename
        with open(filepath, "wb") as fd:
            fd.write(image_res.content)

        # opens album cover 
        album_image = open(filepath,"rb").read()

    # downloads tracks
    procs = []
    for track in album_info["track"]["itemListElement"]:
        # track number and track name
        pos = track["position"]
        item = track["item"]
        name = item["name"]

        # file link
        additional_property = item["additionalProperty"]
        file_link = [prop["value"] for prop in additional_property if prop["name"].startswith("file")][0]

        # track request
        track_res = requests.get(file_link)
        # checks for errors
        track_res.raise_for_status()

        # saves track
        print(f"Downloading Track {pos} - {name} - By {album_artist}")
        if wav:
            proc = Process(target=wav_save,args=(album_dir, name, track_res, pos))
            procs.append(proc)
            proc.start()
        else:
            mp3_save(album_dir, name, track_res, pos)

        # adds tags
        if metadata == True and wav == False:
            filename = f"{pos} - {name}.mp3"
            filepath = album_dir / filename
            tag(filepath, album_image, album_artist, album_name, name, pos)
    
    for proc in procs:
        proc.join()

def tag(filepath, album_image, album_artist, album_name, track_name, track_num):
    # adds tags to the track
    audiofile = eyed3.load(filepath)
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.artist = album_artist
    audiofile.tag.album = album_name
    audiofile.tag.album_artist = album_artist
    audiofile.tag.title = track_name
    audiofile.tag.track_num = track_num

    front_cover = 3
    audiofile.tag.images.set(front_cover,album_image,"image/jpeg")

    # saves tags
    audiofile.tag.save()

def mp3_save(dir, name, track, pos):
    filename = f"{pos} - {name}.mp3"
    filepath = dir / filename
    with open(filepath, "wb") as fd:
        fd.write(track.content)

def wav_save(dir, name, track, pos):
    filename = f"{pos} - {name}.wav"
    filepath = dir / filename
    AudioSegment.from_mp3(BytesIO(track.content)).export(filepath, format="wav", bitrate="128k")


if __name__ == '__main__': 
    # reads the link to the album
    parser = argparse.ArgumentParser(description="Downloads albums from bandcamp")
    parser.add_argument("link", metavar="LINK", type=str, help="Album link")
    parser.add_argument("dir", metavar="DIR", type=str, help="Output Dir")
    args = parser.parse_args()
    link = args.link
    album_dir = args.dir
    # downloads the album
    download(link, album_dir, wav=False, metadata=True)