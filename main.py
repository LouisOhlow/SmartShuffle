import os
import random
from tkinter import *
from tkinter.filedialog import askdirectory

from mutagen.id3 import ID3

import pygame

#  create the window with tkinter
root = Tk()
root.minsize(300, 300)
# create list to store the mp3 data, the list of the song titles and their rating
playlist = []
titles = []

title_label = StringVar()

index = 0  # index for the song currently choosed


def smart_shuffle(event):  # function to choose the song by smart shuffle
    global index
    songs_above_rating = []
    ran = random.uniform(0.1, 1.0)  # rate limit for the new songs
    ratelist_index = -1  # manual index for the loop
    
    # adds all the songs to the list which are above the rating - the better the rating
    # the more possible is it to be selected
    for i in ratelist:  
        ratelist_index += 1
        if i > ran:
            songs_above_rating.append(playlist[ratelist_index])

    shuffled_track = random.choice(songs_above_rating) # selects random song from the new playlist
    pygame.mixer.music.load(shuffled_track)
    pygame.mixer.music.play()
    index = playlist.index(shuffled_track)  # changes the index to the current song
    update_label()


def correct_rate(self):
    global ratelist
    self.songs.sort(key=lambda tracks: tracks.rate, reverse=True)
    correct_multi = 1.0 / self.songs[0].rate
    for l in ratelist:
        l.correct_rate(correct_multi)

def continue_song(event): #  continues the song
    pygame.mixer.music.unpause()


def next_song(event): #  plays next song
    global index
    index += 1
    if index > len(playlist)-1:
        index = 0
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    update_label()


def prev_song(event): #  selects previous song
    global index
    index -= 1
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    update_label()


def pause_song(event):
    pygame.mixer.music.pause()
    title_label.set


def shuffle_song(event): # selects a random song
    global index
    index = playlist.index(random.choice(playlist))
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    update_label()


def update_label(): #  updates the variable label to show which song is playing
    global index
    title_label.set(titles[index])


def directory_chooser(): #  chooses the directory for the songs and saves it in th list
    global ratelist
    directory = askdirectory() #  method to choose the directory
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith('.mp3'):  # add all files which are mp3 files

            path = os.path.realpath(files)  # gets the directory for ID3
            audio = ID3(path)
            titles.append(audio.get("TIT2"))
            playlist.append(files)
    playlist.reverse() #  reverse so the song which is player is on top
    pygame.mixer.init()
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    ratelist = [1.0] * len(playlist)  # adds a rating to every song entry

directory_chooser()


header_label = Label(root, text='Smart Shuffle Proto')
header_label.pack()

listbox = Listbox(root)
listbox.pack()

for songs in titles:
    listbox.insert(0, songs)

titles.reverse()
update_label()

unpause_button = Button(root, text='Play')
unpause_button.pack()
unpause_button.bind("<Button-1>", continue_song)

next_button = Button(root, text='Next Song')
next_button.pack()
next_button.bind("<Button-1>", next_song)

previous_button = Button(root, text='Previous Song')
previous_button.pack()
previous_button.bind("<Button-1>", prev_song)

pause_button = Button(root, text='Stop')
pause_button.pack()
pause_button.bind("<Button-1>", pause_song)

shuffle_button = Button(root, text='Shuffle')
shuffle_button.pack()
shuffle_button.bind("<Button-1>", shuffle_song)

smart_shuffle_button = Button(root, text='SmartShuffle')
smart_shuffle_button.pack()
smart_shuffle_button.bind("<Button-1>", smart_shuffle)

songTitle = Label(root, textvariable=title_label)
songTitle.pack()


root.mainloop()

#  labelsLibrary = https://www.tutorialspoint.com/python/tk_label.htm
