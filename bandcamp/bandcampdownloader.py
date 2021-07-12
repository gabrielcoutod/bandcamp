import requests
import bs4
import eyed3
import json
import argparse

# reads the link to the album
parser = argparse.ArgumentParser(description="Downloads albums from bandcamp")
parser.add_argument("link", metavar="LINK", type=str, help="Album link")
link = parser.parse_args().link

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


print(f"Downloading Album {album_name} - By {album_artist}")


# downloads album cover
print("Downloading Album cover")
album_image_link = album_info["image"]
image_res = requests.get(album_image_link)
#checks for errors
image_res.raise_for_status()

# saves the album cover
filename = "cover.jpg"
with open(filename, "wb") as fd:
    for chunk in image_res.iter_content(chunk_size=100000):
        fd.write(chunk)


# opens album cover 
album_image = open("cover.jpg","rb").read()

# downloads tracks and adds tags 
for track in album_info["track"]["itemListElement"]:
    # track number and track name
    pos = track["position"]
    item = track["item"]
    name = item["name"]

    print(f"Downloading Track {pos} - {name} - By {album_artist}")

    # file link
    additional_property = item["additionalProperty"]
    file_link = [prop["value"] for prop in additional_property if prop["name"].startswith("file")][0]

    # track request
    track_res = requests.get(file_link)
    # checks for errors
    track_res.raise_for_status()

    # saves track
    filename = f"{name}.mp3"
    with open(filename, "wb") as fd:
        for chunk in track_res.iter_content(chunk_size=100000):
            fd.write(chunk)

    # adds tags to the track
    audiofile = eyed3.load(filename)
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.artist = album_artist
    audiofile.tag.album = album_name
    audiofile.tag.album_artist = album_artist
    audiofile.tag.title = name
    audiofile.tag.track_num = pos

    front_cover = 3
    audiofile.tag.images.set(front_cover,album_image,"image/jpeg")

    # saves tags
    audiofile.tag.save()