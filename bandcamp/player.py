import os
from re import S
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
from pydub import AudioSegment
import curses
from pathlib import Path
from pydub.utils import mediainfo


class Player:
    '''
    Class for playing music
    '''

    def __init__(self, album):
        self.album = album
        self.playing = False 
        self.paused = False
        self.current_song = 0

        # song names
        self.song_names = []
        for songfile in self.album:
            song_name = songfile
            song_name = song_name[song_name.rfind('/'):] # removes dirs
            song_name = song_name[song_name.find('-') + 2:] # removes track number and '-'
            song_name = song_name[:-4] #removes extension
            self.song_names.append(song_name)

    def setPaused(self, bool_val):
        self.paused = bool_val

    def setPlaying(self, bool_val):
        self.playing = bool_val 

    def isPlaying(self):
        return self.playing
    
    def isPaused(self):
        return self.paused

    def get_status(self):
        if not self.isPlaying():
            return "Not Playing"
        elif self.isPaused():
            return f"Paused {self.song_names[self.current_song]}"
        else:
            return f"Playing {self.song_names[self.current_song]}"
    
    def play(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        self.setPlaying(True)
        self.setPaused(False)

    def pause(self):
        pygame.mixer.music.pause()
        self.setPaused(True)

    def unpause(self):
        pygame.mixer.music.unpause()
        self.setPaused(False)
    
    def interface(self):
        curses.wrapper(lambda x: self.menu(x))

    
    def menu(self, stdscr):

        # starts mixer
        pygame.mixer.init()

        # starts screen
        stdscr.clear()
        stdscr.refresh()

        # starts colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # interface values
        selected_song = 0
        pressed_key = ''
        first_song = 0
        last_song = len(self.album) - 1 

        # no blocking
        stdscr.nodelay(True)

        # main loop
        while pressed_key != ord('q'):

            song_ended = self.isPlaying() and not self.isPaused() and not pygame.mixer.music.get_busy()
            
            if pressed_key != curses.ERR or song_ended:
                
                # initialization
                stdscr.clear()
                height, width = stdscr.getmaxyx()

                # checks if song ended
                if song_ended:
                    if self.current_song < last_song:
                        self.current_song += 1
                        self.play(self.album[self.current_song])
                    else:
                        self.current_song = 0
                        self.setPlaying(False)

                # checks pressed keys
                if pressed_key == curses.KEY_DOWN:
                    if selected_song < last_song:
                        selected_song += 1
                elif pressed_key == curses.KEY_UP:
                    if selected_song > first_song:
                        selected_song -= 1
                elif pressed_key == ord('p'):
                    if self.isPlaying():
                        if self.isPaused():
                            self.unpause()
                        else:
                            self.pause()
                    else:
                        self.play(self.album[self.current_song])
                elif pressed_key == ord('s'):
                    self.play(self.album[selected_song])
                    self.current_song = selected_song

                # help and status text 
                help_text = f"Press 'q' to exit | Press 'p' to play/pause | Press 's' to (re)start song"
                song_status = self.get_status()

                # writes help and status
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(height-1, 0, song_status)
                stdscr.addstr(height-1, len(song_status), " " * (width - len(song_status) - 1))
                stdscr.addstr(0, 0, help_text)
                stdscr.addstr(0, len(help_text), " " * (width - len(help_text) - 1))
                stdscr.attroff(curses.color_pair(3))

                # writes song info on the screen
                for i in range(len(self.album)):

                    color = 2 if i == self.current_song else 1
                    stdscr.attron(curses.color_pair(color))
                    song_info = f"{i+1} {self.song_names[i]}"
                    stdscr.addstr(i+1, 0, song_info)
                    stdscr.attroff(curses.color_pair(color))

                # refresh
                stdscr.refresh()
                stdscr.move(selected_song + 1, 0)

            # reads input
            pressed_key = stdscr.getch()



def main():
    # parses album folder
    parser = argparse.ArgumentParser(description="plays albums")
    parser.add_argument("album_folder", metavar="ALBUM", type=str, help="Album folder")
    args = parser.parse_args()
    album_folder = Path(args.album_folder)

    # gets the filenames
    mp3_album = []
    for file in album_folder.glob("*.mp3"):
        mp3_album.append(file.__str__())


    mp3_album.sort(key=lambda x: mediainfo(x)["TAG"]["track"])


    # converts the files to wav
    album = []
    for file in mp3_album:
        new_file_name = file[:-3] + "wav"
        AudioSegment.from_mp3(file).export(new_file_name, format="wav")
        album.append(new_file_name)

    # stars the player
    player = Player(album)
    player.interface()

    # deletes wav files
    for file in album:
        Path(file).unlink()

if __name__ == "__main__":
    main()