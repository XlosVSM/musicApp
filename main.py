###########
# Imports #
###########
# GUI Creation
from tkinter import *
from tkinter import ttk  # So I can use themed widgets
from ttkthemes import ThemedStyle  # Gives access to amazing Tkinter ttk themes
from PIL import Image, ImageTk

# Music
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Stop pygame's welcome message popping up in console
from pygame import mixer
from mutagen.wave import WAVE

# Miscellaneous
from pandas import read_json
from random import choice
from os import listdir, remove
from sys import platform

###########
# Classes #
###########
# The core of the app
class musicApp(Tk):
    def __init__(self):
        global appTheme
        
        Tk.__init__(self)
        
        # Style the code
        self.title("Music App")
        self.state("zoomed")
        self.style = ThemedStyle(self)
        try:
            self.style.set_theme(appTheme)
        
        # If theme.txt is tampered with, it will delete the file and rewrite it
        except TclError:
            remove("theme.txt")
            appTheme = createThemeFile()
            self.style.set_theme(appTheme)
        
        # Open on the starting page
        self._frame = None
        self.switchPage(StartPage)
    
    def addMenuBar(self, menuName, commands):  # Create the menu bar
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
    def switchPage(self, frameClass):  # Switch between pages
        # Stop music from playing
        for x in range(5):
            mixer.Channel(x).stop()
        
        newFrame = frameClass(self)
        
        if self._frame is not None:
            self._frame.destroy()
            
        self._frame = newFrame
        self._frame.pack()

    def changeTheme(self, currentState):  # Change the program's theme when the button is clicked
        global appTheme
        
        if currentState == "equilux":
            newState = "yaru"
        
        else:
            newState = "equilux"
        
        self.style.theme_use(newState)
        appTheme = newState
        
        with open('theme.txt', 'w') as i:
            i.write(newState)
    
    def changePlaySoundTestVariable(self, currentState):
        global playTestSound
        
        if currentState == True:
            newState = False
            
        else:
            newState = True
        
        playTestSound = newState
        
        with open('testSound.txt', 'w') as i:
            i.write(str(newState))
                        
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
        
        self.intervalsButton = ttk.Button(self, text = "Intervals", command = lambda: master.switchPage(IntervalsTutorialPage))
        self.intervalsButton.grid(row = 2, column = 1, sticky = N + S + E + W)
        
        self.chordsButton = ttk.Button(self, text = "\n\n\nChords\n\n\n")
        self.chordsButton.grid(row = 2, column = 2, sticky = N + S + E + W)
        
        self.terminologyButton = ttk.Button(self, text = "  Terminology   ")
        self.terminologyButton.grid(row = 3, column = 1, sticky = N + S + E + W)
        
        self.instrumentPracticeButton = ttk.Button(self, text = "\n\nInstrument\nPractice\n\n", command =  lambda: master.switchPage(MusicSelectorPage))
        self.instrumentPracticeButton.grid(row = 3, column = 2, sticky = N + S + E + W)

# Intervals tutorial
class IntervalsTutorialPage(ttk.Frame):
    def __init__(self, master):
        global intervalExampleImg
        
        ttk.Frame.__init__(self, master)
        
        intervalExampleImage = Image.open("images/exampleIntervals.png")  # Hyacinth, CC BY-SA 3.0, via Wikimedia Commons+
        intervalExampleImg = ImageTk.PhotoImage(intervalExampleImage)
        self.intervalExampleImageLabel = Label(self, image = intervalExampleImg)
        self.intervalExampleImageLabel.pack()
        
        informationLabel = ttk.Label(self, text = '''Intervals is the distance between two notes. Above is a picture showing what all the\nintervals will look like at the tonic of middle C. The way to tell what the interval is by\ncounting how many lines and gaps there are between the notes starting on the first note.\nFor example, a perfect fourth would have 4 lines and gaps in between it.\n''', font = ("TkDefaultFont", 20), justify =  CENTER)
        informationLabel.pack()
        
        harmonicIntervalTestButton = ttk.Button(self, text = "Harmonic Interval Test", command = lambda: master.switchPage(HarmonicIntervalsTest))
        harmonicIntervalTestButton.pack()
        
        melodicIntervalTestButton = ttk.Button(self, text = "Melodic Interval Test")
        melodicIntervalTestButton.pack()

# Harmonic intervals test
class HarmonicIntervalsTest(ttk.Frame):
    def __init__(self, master):
        global intervalImg
        
        ttk.Frame.__init__(self, master)
        
        # Add score counter
        self.score = 0
        self.scoreCounter = ttk.Label(self, text = "Score: " + str(self.score), font = ("TkDefaultFont", 32))
        self.scoreCounter.pack()
        
        self.imageFolderOptions = listdir("images/intervals/harmonic")
        
        # Get rid of the .DS_Store file as it crashes code
        if platform == "darwin":  # if the operating system is a Mac
            self.imageFolderOptions.remove('.DS_Store')
        
        self.selectRandomImage()      
        
        intervalImage = Image.open("images/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
        intervalImg = ImageTk.PhotoImage(intervalImage)
        self.intervalImageInterval = Label(self, image = intervalImg)
        self.intervalImageInterval.pack()
        
        if playTestSound is True:
            self.playMIDI("music/midi/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
        
        self.p5Button = ttk.Button(self, text = "P5", command = lambda: self.buttonClicked("P5"))
        self.p5Button.pack()
        
        self.octaveButton = ttk.Button(self, text = "Octave", command = lambda: self.buttonClicked("Octave"))
        self.octaveButton.pack()
    
    def selectRandomImage(self):
        self.imageFolder = choice(self.imageFolderOptions)
        imagePitchOptions = listdir("images/intervals/harmonic/" + self.imageFolder)
        self.testImage = choice(imagePitchOptions)
    
    def buttonClicked(self, selectedButton):
        global newImg
        
        if selectedButton == self.imageFolder:
            self.score += 1
            self.scoreCounter.config(text = "Score: " + str(self.score))
        
        self.selectRandomImage()
        
        newImage = Image.open("images/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
        newImg = ImageTk.PhotoImage(newImage)
        self.intervalImageInterval.configure(image = newImg)
        
        if playTestSound is True:
            self.playMIDI("music/midi/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
    
    def playMIDI(self, midiFile):       
        musicFile = midiFile.replace('.png', '.mid')
        
        mixer.music.load(musicFile)
        mixer.music.play()

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
        self.albumCoverLabel.grid(rowspan = 6, columnspan = 6)
        
        songName = ttk.Label(self, text = "Title: " + chosenSongTitle + " ", font = ("Helvetica", 20), justify = CENTER)
        songName.grid(row = 0, column = 6, columnspan = 3)
        
        artistName = ttk.Label(self, text = "Artist: " + chosenSongArtist + " ", font = ("Helvetica", 20), justify = CENTER)
        artistName.grid(row = 2, column = 6, columnspan = 3)
        
        albumName = ttk.Label(self, text = "Album: " + chosenSongAlbum + " ", font = ("Helvetica", 20), justify = CENTER)
        albumName.grid(row = 4, column = 6, columnspan = 3)
        
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
        
        # Create the volume sliders for the mixer tracks
        # Bass slider
        self.bassSlider = Scale(self, from_ = 100, to = 0, command = self.bassVolume)
        if appTheme == "equilux":
            self.bassSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.bassSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.bassSlider.set(100)
        self.bassSlider.grid(row = 9, column = 0)
        
        self.bassSliderLabel = ttk.Label(self, text = "Bass", wraplength = 1, justify = CENTER)
        self.bassSliderLabel.grid(row = 9, column = 1, sticky = W)
        
        # Drums slider
        self.drumsSlider = Scale(self, from_ = 100, to = 0, command = self.drumsVolume)
        if appTheme == "equilux":
            self.drumsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.drumsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.drumsSlider.set(100)
        self.drumsSlider.grid(row = 9, column = 2)
        
        self.drumsSliderLabel = ttk.Label(self, text = "Drums", wraplength = 1, justify = CENTER)
        self.drumsSliderLabel.grid(row = 9, column = 3, sticky = W)
        
        # Other slider
        self.otherSlider = Scale(self, from_ = 100, to = 0, command = self.otherVolume)
        if appTheme == "equilux":
            self.otherSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.otherSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.otherSlider.set(100)
        self.otherSlider.grid(row = 9, column = 4)
        
        self.otherSliderLabel = ttk.Label(self, text = "Other", wraplength = 1, justify = CENTER)
        self.otherSliderLabel.grid(row = 9, column = 5, sticky = W)
        
        # Piano slider
        self.pianoSlider = Scale(self, from_ = 100, to = 0, command = self.pianoVolume)
        if appTheme == "equilux":
            self.pianoSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.pianoSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.pianoSlider.set(100)
        self.pianoSlider.grid(row = 9, column = 6)
        
        self.pianoSliderLabel = ttk.Label(self, text = "Piano", wraplength = 1, justify = CENTER)
        self.pianoSliderLabel.grid(row = 9, column = 7, sticky = W)
        
        # Vocals slider
        self.vocalsSlider = Scale(self, from_ = 100, to = 0, command = self.vocalVolume)
        if appTheme == "equilux":
            self.vocalsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.vocalsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.vocalsSlider.set(100)
        self.vocalsSlider.grid(row = 9, column = 8)
        
        self.vocalsSliderLabel = ttk.Label(self, text = "Vocals", wraplength = 1, justify = CENTER)
        self.vocalsSliderLabel.grid(row = 9, column = 9, sticky = W)
    
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
       
    def vocalVolume(self, x):  # Making the sliders change their corresponding mixer channel's volume
        volume = self.vocalsSlider.get() / 100
        self.channel5.set_volume(volume)
        
# The settings page       
class SettingsPage(ttk.Frame):
    def __init__(self, master):        
        ttk.Frame.__init__(self, master)
        
        self.darkModeCheckbox = ttk.Checkbutton(self, text = "Dark Mode", command = lambda: master.changeTheme(appTheme))
        
        if appTheme == "equilux":
            self.darkModeCheckbox.state(["selected"])
        
        self.darkModeCheckbox.pack()
        
        self.playTestMusicCheckbox = ttk.Checkbutton(self, text = "Play music in tests", command = lambda: master.changePlaySoundTestVariable(playTestSound))
        
        if playTestSound is True:
            self.playTestMusicCheckbox.state(["selected"])
        
        self.playTestMusicCheckbox.pack()
        
# About page
class AboutPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        aboutText = ttk.Label(self, text = '''My intended outcome is to make a Graphical User Interface (GUI) to help people learn aspects of music theory, understand some musical\nfundamentals, and practice their instruments.  A particularly innovative feature I want to include is a music player that users can customise to hear\nwhat they want. For example, vocals can be removed from a track so the user can use it like a karaoke machine. Alternatively, the bass can be\n removed from the track if the user wants to practice bass by playing along with the songs.\n\nIn the market today, some apps and programs do have these functions, only with some significant drawbacks. They are either pay-to-use, averaging NZ$8.99\n(like the ABRSM Aural Trainer app), too complicated for my age group (like the UCLA Music Theory app), or too basic to be useful (like Mussila Music). My\n program will be free to use, contain the necessary lessons that beginners can use intuitively, and contain some fun play-along features not available in other apps. ''', font = ("TkDefaultFont", 20), justify = CENTER)
        aboutText.pack()
        
###############
# Definitions #
###############     
def createThemeFile(): 
    from darkdetect import isDark
    
    if isDark() is True:
        appTheme = "equilux"
    
    else:
        appTheme = "yaru"
        
    # Create a file so the code uses the theme next time the user runs the code
    with open('theme.txt', 'w') as i:
        i.write(appTheme)
    
    return appTheme

# A blank pass for the unavailable pages as the program requires a definition for the button's command, and the pass command is not accepted
def null():
    pass

def createMenuBar():
    menuBar = MenuBar(app)
    
    # Instrument roles cascade
    menuBar.addMenuBar(
        "Instrument Roles", commands = [
            ("Rock Band", null)
        ],
    )

    # Sight reading cascade
    menuBar.addMenuBar(
        "Sight Reading", commands = [
            ("Tutorial", null),
            ("Test", null)
        ]
    )
    
    # Intervals cascade
    menuBar.addMenuBar(
        "Intervals", commands = [
            ("Tutorial", lambda: app.switchPage(IntervalsTutorialPage)),
            ("Harmonic", lambda: app.switchPage(HarmonicIntervalsTest)),
            ("Melodic", null)
        ]
    )
    
    # Chords cascade
    menuBar.addMenuBar(
        "Chords", commands = [
            ("Tutorial", null),
            ("Chord Quality", null),
            ("Cadences", null),
        ]
    )
    
    # Terminology cascade
    menuBar.addMenuBar(
        "Terminology", commands = [
            ("Tutorial", null),
            ("Flash Cards", null)
        ]
    )
    
    # Instrument practice cascade
    menuBar.addMenuBar(
        "Instrument Practice", commands = [
            ("Choose Song", lambda: app.switchPage(MusicSelectorPage))
        ]
    )
        
    # Preferences cascade
    menuBar.addMenuBar(
        "Preferences", commands = [
            ("Settings", lambda: app.switchPage(SettingsPage)),
            ("About", lambda: app.switchPage(AboutPage))
        ]
    )

#############
# Main code #
#############   
if __name__ == "__main__":
    # Try getting the user's preferred theme
    try:
        with open('theme.txt') as i:
            appTheme = i.readline()
    
    # First time use or missing theme.txt
    except FileNotFoundError:
        appTheme = createThemeFile()
    
    # Try getting the user's preference on sound in test
    try:
        with open('testSound.txt') as i:
            playTestSound = bool(i.readline())
    
    except FileNotFoundError:
        with open('testSound.txt', 'w') as i:
            i.write("True")
        
        playTestSound = True
    
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
    app = musicApp()
        
    createMenuBar()
    
    app.mainloop()
