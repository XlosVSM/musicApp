####### Imports #######
# GUI Creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle # Gives access to amazing Tkinter ttk themes without having to spend time designing my own one
from PIL import Image, ImageTk

# Music
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Stop pygame's welcome message popping up in console
from pygame import mixer
from mutagen.wave import WAVE
try:
    from musicalbeeps import Player # To play to notes in test # https://pypi.org/projexct/musicalbeeps/

except ModuleNotFoundError: # This helps users have a better understanding on how to get the package to work
    from termcolor import colored
    
    link = colored("https://visualstudio.microsoft.com/visual-cpp-build-tools/", "blue")
    print('This program requires the module musicalbeeps. This package does require Microsoft Visual C++ 14.0 or greater. Download "Microsoft C++ Build Tools" from ' + link + ' to get it. Select "Desktop development with C++" to ensure you install everything needed. Do this before doing pip install musicalbeeps. If you are using a Mac, you will not need to install this.')
    exit()

# Misc (termcolor is only imported when there is an error)
from pandas import read_json
from random import choice
from os import listdir

# https://commons.wikimedia.org/wiki/File:Perfect_intervals_on_C.png

####### Classes #######
# The core of the app.
class musicApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        # Style the code
        self.title("Music App")
        self.state("zoomed")
        self.style = ThemedStyle(self)
        self.style.set_theme(appTheme)
        
        # Open on the starting page
        self._frame = None
        self.switchPage(StartPage)
    
    def addMenuBar(self, menuName, commands): # Create the menu bar
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)        
    
    def switchPage(self, frameClass): # Switch between pages
        # Stop music from playing
        for x in range(5):
            mixer.Channel(x).stop()
        
        newFrame = frameClass(self)
        
        if self._frame is not None:
            self._frame.destroy()
            
        self._frame = newFrame
        self._frame.pack()

    def changeTheme(self, theme): # Change the program's theme when the button is clicked
        global appTheme
        
        if theme == "equilux":
            theme = "yaru"
        
        else:
            theme = "equilux"
        
        self.style.theme_use(theme)
        appTheme = theme
        
        with open('theme.txt', 'w') as i:
            i.write(theme)
        
        if appTheme == "equilux":
            toggleButton['text'] = "Dark Mode"
            
        else:
            toggleButton['text'] = "Light Mode"

# The menu bar
class MenuBar():
    def __init__(self, parent):
        self.menuBar = Menu(parent)
        self.create()
        
    def create(self):
        app.config(menu = self.menuBar)
        
    def addMenuBar(self, menuName, commands):
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)

# The opening page
class StartPage(ttk.Frame):
    def __init__(self, master):
        global trebleImg # Images must be global so they can be seen
        
        ttk.Frame.__init__(self, master)
        self.grid(sticky = N + S + E + W)
        
        # Configure the grid's columns
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(4, weight = 1)
        self.grid_columnconfigure(4, weight = 1)
        
        # Configure the grid's rows
        self.rowconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 0)
        
        self.header = ttk.Label(self, text = " Music Learning App ", font = ("Helvetica", 64))
        self.header.grid(row = 0, columnspan = 5, sticky = E + W)
        
        trebleImage = Image.open("images/trebleClef.png")
        trebleImg = ImageTk.PhotoImage(trebleImage)
        self.trebleImageLabel = Label(self, image = trebleImg)
        self.trebleImageLabel.grid(rowspan = 4, column = 0)
        
        self.instrumentRoleButton = ttk.Button(self, text = "Instrument Roles")
        self.instrumentRoleButton.grid(row = 1, column = 1, sticky = N + S + E + W)
        
        self.sightReadingButton = ttk.Button(self, text = "\n\n\n  Sight Reading \n\n\n")
        self.sightReadingButton.grid(row = 1, column = 2, sticky = N + S + E + W)
        
        self.intervalsButton = ttk.Button(self, text = "Intervals")
        self.intervalsButton.grid(row = 2, column = 1, sticky = N + S + E + W)
        
        self.chordsButton = ttk.Button(self, text = "\n\n\nChords\n\n\n")
        self.chordsButton.grid(row = 2, column = 2, sticky = N + S + E + W)
        
        self.terminologyButton = ttk.Button(self, text = "  Terminology   ")
        self.terminologyButton.grid(row = 3, column = 1, sticky = N + S + E + W)
        
        self.instrumentPracticeButton = ttk.Button(self, text = "\n\nInstrument\nPractice\n\n", command =  lambda: app.switchPage(MusicSelectorPage))
        self.instrumentPracticeButton.grid(row = 3, column = 2, sticky = N + S + E + W)

# Harmonic intervals test
class HarmonicIntervalsTest(ttk.Frame):
    def __init__(self, master):
        global intervalImage
        
        ttk.Frame.__init__(self, master)
        
        player = Player(volume = 0.3, mute_output = False)
        
        imageFolder = choice(listdir("images/intervals/harmonic"))
        print(imageFolder)
        intervalImage = choice(listdir("images/intervals/harmonic/P5"))

# List of all the songs users can practice along to
class MusicSelectorPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        for song in range(dfRange):
            ttk.Button(self, text = songNameList[song], command = lambda i=song: self.playSong(i)).pack()
        
    def playSong(self, chosenSong):
        global selectedSong, songFile
        
        folders = df.loc[:, "Folder"]
        folderList = folders.tolist()
        
        songFile = folderList[chosenSong]
        selectedSong = chosenSong
        
        app.switchPage(MusicPlayerPage)

# The music player 
class MusicPlayerPage(ttk.Frame):
    def __init__(self, master):
        # Credit for play/pause buttons: © 2014 Andreas Kainz & Uri Herrera & Andrew Lake & Marco Martin & Harald Sitter & Jonathan Riddell & Ken Vermette & Aleix Pol & David Faure & Albert Vaca & Luca Beltrame & Gleb Popov & Nuno Pinheiro & Alex Richardson & Jan Grulich & Bernhard Landauer & Heiko Becker & Volker Krause & David Rosca & Phil Schaf / KDE
        global albumCoverImg
        
        ttk.Frame.__init__(self, master)
        
        # Call the corresponding song data
        chosenSongTitle = songNameList[selectedSong]
        chosenSongArtist = songArtistList[selectedSong]
        chosenSongAlbum = songAlbumList[selectedSong]
        albumFile = albumCoverList[selectedSong]
        
        # Create the song information
        albumCover = Image.open("images/albumCovers/" + albumFile)
        albumCoverImg = ImageTk.PhotoImage(albumCover)
        self.albumCoverLabel = Label(self, image = albumCoverImg)
        self.albumCoverLabel.grid(rowspan = 3, columnspan = 3)
        
        songName = ttk.Label(self, text = "Title: " + chosenSongTitle + " ", font = ("Helvetica", 20))
        songName.grid(row = 0, column = 4)
        
        artistName = ttk.Label(self, text = "Artist: " + chosenSongArtist + " ", font = ("Helvetica", 20))
        artistName.grid(row = 1, column = 4)
        
        albumName = ttk.Label(self, text = "Album: " + chosenSongAlbum + " ", font = ("Helvetica", 20))
        albumName.grid(row = 2, column = 4)
        
        # Play the song
        self.file = "music/stems/" + songFile
        
        self.channel1 = mixer.Channel(0)
        channel1Sound = mixer.Sound(self.file + "/bass.wav")
        self.channel1.play(channel1Sound)

        self.channel2 = mixer.Channel(1)
        channel2Sound = mixer.Sound(self.file + "/drums.wav")
        self.channel2.play(channel2Sound)

        self.channel3 = mixer.Channel(2)
        channel3Sound = mixer.Sound(self.file + "/other.wav")
        self.channel3.play(channel3Sound)

        self.channel4 = mixer.Channel(3)
        channel4Sound = mixer.Sound(self.file + "/piano.wav")
        self.channel4.play(channel4Sound)

        self.channel5 = mixer.Channel(4)
        channel5Sound = mixer.Sound(self.file + "/vocals.wav")
        self.channel5.play(channel5Sound)
        
        # Add the progress bar
        song = WAVE(self.file + "/bass.wav") # Any of the files would work
        songDuration = song.info.length
        
        self.progressBar = ttk.Scale(self, from_ = 0, to = songDuration, orient = HORIZONTAL, length = 520)
        
        self.progressBar.bind("<ButtonRelease-1>", self.updateValue)
        self.progressBar.set(0)
        self.progressBar.grid(row = 4, columnspan = 5)
        
        # Create the volume sliders for the mixer tracks
        # Bass slider
        self.bassSlider = Scale(self, from_ = 100, to = 0, command = self.bassVolume)
        if appTheme == "equilux":
            self.bassSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.bassSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.bassSlider.set(100)
        self.bassSlider.grid(row = 5, column = 0)
        
        # Drums slider
        self.drumsSlider = Scale(self, from_ = 100, to = 0, command = self.drumsVolume)
        if appTheme == "equilux":
            self.drumsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.drumsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.drumsSlider.set(100)
        self.drumsSlider.grid(row = 5, column = 1)
        
        # Other slider
        self.otherSlider = Scale(self, from_ = 100, to = 0, command = self.otherVolume)
        if appTheme == "equilux":
            self.otherSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.otherSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.otherSlider.set(100)
        self.otherSlider.grid(row = 5, column = 2)
        
        # Piano slider
        self.pianoSlider = Scale(self, from_ = 100, to = 0, command = self.pianoVolume)
        if appTheme == "equilux":
            self.pianoSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.pianoSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.pianoSlider.set(100)
        self.pianoSlider.grid(row = 5, column = 3)
        
        # Vocals slider
        self.vocalsSlider = Scale(self, from_ = 100, to = 0, command = self.vocalVolume)
        if appTheme == "equilux":
            self.vocalsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.vocalsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.vocalsSlider.set(100)
        self.vocalsSlider.grid(row = 5, column = 4)
    
    def updateValue(self, event):
        channel4Sound = mixer.Sound(self.file + "/piano.wav")
        self.channel4.play(channel4Sound)
    
    def bassVolume(self, x):
        volume = self.bassSlider.get() / 100
        self.channel1.set_volume(volume)
        
    def drumsVolume(self, x):
        volume = self.drumsSlider.get() / 100
        self.channel2.set_volume(volume)
       
    def otherVolume(self, x):
        volume = self.otherSlider.get() / 100
        self.channel3.set_volume(volume)
        
    def pianoVolume(self, x):
        volume = self.pianoSlider.get() / 100
        self.channel4.set_volume(volume)
       
    def vocalVolume(self, x): # Making the sliders change their corresponding mixer channel's volume
        volume = self.vocalsSlider.get() / 100
        self.channel5.set_volume(volume)
        
# The settings page       
class SettingsPage(ttk.Frame):
    def __init__(self, master):
        global toggleButton
        ttk.Frame.__init__(self, master)
        
        ttk.Label(self, text = "WE HERE NOW").pack()
        
        # Making sure that the button opens on the corresponding mode
        if appTheme == "equilux":
            modeText = "Dark Mode"
            
        else:
            modeText = "Light Mode"
        
        toggleButton = ttk.Button(self, text = modeText, width = 10, command = lambda: master.changeTheme(theme = appTheme))
        toggleButton.pack()
        
        ttk.Button(self, text = "Home", command = lambda: master.switchPage(StartPage)).pack()
        
####### Definitions ########      
def createThemeFile(): 
    from darkdetect import isDark
    
    if isDark() == True:
        appTheme = "equilux"
    
    else:
        appTheme = "yaru"
        
    # Create a file so the code uses the theme next time the user runs the code
    with open('theme.txt', 'w') as i:
        i.write(appTheme)
    
    return appTheme

# A blank pass for the unavailable pages as the program requires a definition for the button's command, and the pass command is not accepted
def menuPass():
    pass

def createMenuBar():
    menuBar = MenuBar(app)
    
    # Instrument roles cascade
    menuBar.addMenuBar(
        "Instrument Roles", commands = [
            ("Rock Band", menuPass, True)
        ],
    )

    # Sight reading cascade
    menuBar.addMenuBar(
        "Sight Reading", commands = [
            ("Tutorial", menuPass, True),
            ("Test", menuPass, True)
        ]
    )
    
    # Intervals cascade
    menuBar.addMenuBar(
        "Intervals", commands = [
            ("Tutorial", menuPass, True),
            ("Harmonic", lambda: app.switchPage(HarmonicIntervalsTest), True),
            ("Melodic", menuPass, True)
        ]
    )
    
    # Chords cascade
    menuBar.addMenuBar(
        "Chords", commands = [
            ("Tutorial", menuPass, True),
            ("Chord Quality", menuPass, True),
            ("Cadences", menuPass, True),
        ]
    )
    
    # Terminology cascade
    menuBar.addMenuBar(
        "Terminology", commands = [
            ("Tutorial", menuPass, True),
            ("Flash Cards", menuPass, True)
        ]
    )
    
    # Instrument practice cascade
    menuBar.addMenuBar(
        "Instrument Practice", commands = [
            ("Choose Song", lambda: app.switchPage(MusicSelectorPage), True)
        ]
    )
        
    # Preferences cascade
    menuBar.addMenuBar(
        "Preferences", commands = [
            ("Settings", lambda: app.switchPage(SettingsPage), True)
        ]
    )

####### Main code #######    
if __name__ == "__main__":
    # Try getting the user's preferred theme
    try:
        with open('theme.txt') as i:
            appTheme = i.readline()
    
    # First time use or missing theme.txt
    except FileNotFoundError:
        appTheme = createThemeFile()
    
    mixer.pre_init(0, -16, 5, 512)
    mixer.init()
    
    # Get the song data
    df = read_json("songInfo.json")
    dfRange = len(df)
    
    # Create lists of the data from the JSON file to speed up the program
    songName = df.loc[:, "Song Name"]
    songNameList = songName.tolist()
    
    songArtist = df.loc[:, "Artist"]
    songArtistList = songArtist.tolist()
    
    songAlbum = df.loc[:, "Album"]
    songAlbumList = songAlbum.tolist()
    
    albumCover = df.loc[:, "Album Cover"]
    albumCoverList = albumCover.tolist()
    
    # Run the app
    try:
        app = musicApp()
    
    # If theme.txt has been altered externally
    except TclError:  
        from termcolor import colored
              
        print(colored("Please delete the file theme.txt and run the code again.", "red"))
        exit()
    
    createMenuBar()
    
    app.mainloop()
