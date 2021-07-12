import bandcampdownloader
from player import Player
import argparse
from pathlib import Path


def play(link):

    # downloads album
    temp_folder = "temp_albums"
    bandcampdownloader.download(link,temp_folder, wav=True, metadata=False)

    # gets file names
    temp_folder_path = Path(temp_folder)
    album = []
    for file in temp_folder_path.glob("*.wav"):
        album.append(file.__str__())

    # sorts filenames
    album.sort(key=lambda x: int(x[x.rfind('/') + 1:x.find(' ')]))

    # stars the player
    player = Player(album)
    player.interface()

    # deletes wav files
    for file in album:
        Path(file).unlink()

    # deletes directory
    temp_folder_path.rmdir()

if __name__ == '__main__':
    # parses album folder
    parser = argparse.ArgumentParser(description="plays albums")
    parser.add_argument("link", metavar="ALBUM", type=str, help="Album link")
    args = parser.parse_args()
    album_link = args.link
    #plays album
    play(album_link)