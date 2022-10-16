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

# Miscellaneous
from pandas import DataFrame, read_json
from darkdetect import isDark
from random import choice
from os import listdir
from sys import platform

###########
# Classes #
###########
# The core of the app
class musicApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        # Style the code
        self.title("Music App")
        self.state("zoomed")
        
        # Get the user's preferences
        try:
            userSettings = read_json("preferences.json")
            self.appTheme = userSettings.loc[0, "State",]
            self.playTestSound = bool(userSettings.loc[1, "State"])
        
        except FileNotFoundError:
            self.appTheme = self.setDefaultTheme()
            self.playTestSound = True
            
            data = [['App Theme', self.appTheme], ['Play Music', 'True']]
            df = DataFrame(data, columns = ['Variable', 'State'])
            
            df.to_json('preferences.json')
        
        self.style = ThemedStyle(self)
        try:
            self.style.set_theme(self.appTheme)
        
        # If theme.txt is tampered with, it will delete the file and rewrite it
        except TclError:
            self.appTheme = self.setDefaultTheme()
            self.style.set_theme(self.appTheme)
        
        # Get the song data
        self.df = read_json("songInfo.json")
        self.dfRange = len(self.df)
    
        # Create lists of the data from the JSON file to speed up the program     
        self.songNameList = self.df.loc[:, "Song Name"].tolist()
        self.songArtistList = self.df.loc[:, "Artist"].tolist()
        self.songAlbumList = self.df.loc[:, "Album"].tolist()
        self.albumCoverList = self.df.loc[:, "Album Cover"].tolist()
        
        self.createMenuBar()
        
        # Open on the starting page
        self._frame = None
        self.switchPage(StartPage)
    
    def setDefaultTheme(self): 
        if isDark() is True:
            appTheme = "equilux"
    
        else:
            appTheme = "yaru"
        
        return appTheme
    
    def null(self):
        pass

    def createMenuBar(self):
        menuBar = MenuBar(self)
    
        # Instrument roles cascade
        menuBar.addMenuBar(
            "Instrument Roles", commands = [
                ("Rock Band", self.null)
            ],
        )

        # Sight reading cascade
        menuBar.addMenuBar(
            "Sight Reading", commands = [
                ("Tutorial", self.null),
                ("Test", lambda: self.switchPage(SightReadingTest))
            ]
        )
    
        # Intervals cascade
        menuBar.addMenuBar(
            "Intervals", commands = [
                ("Tutorial", lambda: self.switchPage(IntervalsTutorialPage)),
                ("Harmonic", lambda: self.switchPage(HarmonicIntervalsTest)),
                ("Melodic", self.null)
            ]
        )
    
        # Chords cascade
        menuBar.addMenuBar(
            "Chords", commands = [
                ("Tutorial", self.null),
                ("Chord Quality", self.null),
                ("Cadences", self.null),
            ]
        )
    
        # Terminology cascade
        menuBar.addMenuBar(
            "Terminology", commands = [
                ("Tutorial", self.null),
                ("Flash Cards", self.null)
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
            
    def switchPage(self, frameClass):  # Switch between pages
        # Stop music from playing
        for mixerChannel in range(5):
            mixer.Channel(mixerChannel).stop()
        
        newFrame = frameClass(self)
        
        if self._frame is not None:
            self._frame.destroy()
            
        self._frame = newFrame
        self._frame.pack()

    def changeTheme(self, currentState):  # Change the program's theme when the button is clicked
        if currentState == "equilux":
            newState = "yaru"
        
        else:
            newState = "equilux"
        
        self.style.theme_use(newState)
        self.appTheme = newState
        
        data = [['App Theme', self.appTheme], ['Play Music', str(self.playTestSound)]]
        df = DataFrame(data, columns = ['Variable', 'State'])
            
        df.to_json('preferences.json')
    
    def changePlaySoundTestVariable(self, currentState):
        if currentState == True:
            newState = False
            
        else:
            newState = True
        
        self.playTestSound = newState
        
        data = [['App Theme', self.appTheme], ['Play Music', str(self.playTestSound)]]
        df = DataFrame(data, columns = ['Variable', 'State'])
            
        df.to_json('preferences.json')
    
    def playMIDI(self, midiFile):       
        musicFile = midiFile.replace('.png', '.mid')
        
        mixer.music.load(musicFile)
        mixer.music.play()

                        
# The menu bar
class MenuBar():
    def __init__(self, master):
        self.menuBar = Menu(master)
        self.create(master)
        
    def create(self, master):
        master.config(menu = self.menuBar)
        
    def addMenuBar(self, menuName, commands):
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)

# The opening page
class StartPage(ttk.Frame):
    def __init__(self, master):       
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
        self.trebleImg = ImageTk.PhotoImage(trebleImage)
        self.trebleImageLabel = Label(self, image = self.trebleImg)
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

# Sight reading test
class SightReadingTest(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        # Question counter
        self.questionCounter = 0
        
        # Add score counter
        self.score = 0
        self.scoreCounter = ttk.Label(self, text = "Score: " + str(self.score) + "/" + str(self.questionCounter), font = ("TkDefaultFont", 32))
        self.scoreCounter.pack()
        
        self.imageFolderOptions = listdir("images/sightReading/")
        
        # Get rid of the .DS_Store file as it crashes code
        if platform == "darwin":  # if the operating system is a Mac
            try:
                self.imageFolderOptions.remove('.DS_Store')
            
            except ValueError:  # In case the user does not open the folder, thus not creating a .DS_Store
                pass
        
        self.selectRandomImage("sightReading")
        
        sightReadingImage = Image.open("images/sightReading/" + self.imageFolder + "/" + self.clef + "/" + self.testImage)
        self.sightReadingImg = ImageTk.PhotoImage(sightReadingImage)
        self.sightReadingImageLabel = Label(self, image = self.sightReadingImg)
        self.sightReadingImageLabel.pack()
        
        self.aFlatButton = ttk.Button(self, text = "Ab", command = lambda: self.buttonClicked(master, "Ab", "sightReading"))
        self.aFlatButton.pack()
        
        self.aButton = ttk.Button(self, text = "A", command = lambda: self.buttonClicked(master, "A", "sightReading"))
        self.aButton.pack()
        
        self.bFlatButton = ttk.Button(self, text = "Bb", command = lambda: self.buttonClicked(master, "Bb", "sightReading"))
        self.bFlatButton.pack()
        
        self.bButton = ttk.Button(self, text = "B", command = lambda: self.buttonClicked(master, "B", "sightReading"))
        self.bButton.pack()
        
        self.cButton = ttk.Button(self, text = "C", command = lambda: self.buttonClicked(master, "C", "sightReading"))
        self.cButton.pack()
        
        self.cSharpButton = ttk.Button(self, text = "C#", command = lambda: self.buttonClicked(master, "C#", "sightReading"))
        self.cSharpButton.pack()
        
        self.dButton = ttk.Button(self, text = "D", command = lambda: self.buttonClicked(master, "D", "sightReading"))
        self.dButton.pack()
        
        self.eFlatButton = ttk.Button(self, text = "Eb", command = lambda: self.buttonClicked(master, "Eb", "sightReading"))
        self.eFlatButton.pack()
        
        self.eButton = ttk.Button(self, text = "E", command = lambda: self.buttonClicked(master, "E", "sightReading"))
        self.eButton.pack()
        
        self.fButton = ttk.Button(self, text = "F", command = lambda: self.buttonClicked(master, "F", "sightReading"))
        self.fButton.pack()
        
        self.fSharpButton = ttk.Button(self, text = "F#", command = lambda: self.buttonClicked(master, "F#", "sightReading"))
        self.fSharpButton.pack()
        
        self.gButton = ttk.Button(self, text = "G", command = lambda: self.buttonClicked(master, "G", "sightReading"))
        self.gButton.pack()
        
        if master.playTestSound is True:
            master.playMIDI("music/midi/sightReading/" + self.testImage)
    
    def selectRandomImage(self, testTopic):
        if testTopic == "sightReading":
            self.imageFolder = choice(self.imageFolderOptions)
            self.clef = choice(listdir("images/" + testTopic + "/" + self.imageFolder))
            imagePitchOptions = listdir("images/" + testTopic + "/" + self.imageFolder + "/" + self.clef)
            self.testImage = choice(imagePitchOptions)
        
        else:
            self.imageFolder = choice(self.imageFolderOptions)
            imagePitchOptions = listdir("images/" + testTopic + "/" + self.imageFolder)
            self.testImage = choice(imagePitchOptions)

    def buttonClicked(self, master, selectedButton, testTopic):
        self.questionCounter += 1
        
        if selectedButton == self.imageFolder:
            self.score += 1
            
        self.scoreCounter.config(text = "Score: " + str(self.score) + "/" + str(self.questionCounter))
        
        self.selectRandomImage("sightReading")
        
        newImage = Image.open("images/" + testTopic + "/" + self.imageFolder + "/" + self.clef + "/" + self.testImage)
        self.newImg = ImageTk.PhotoImage(newImage)
        self.sightReadingImageLabel.configure(image = self.newImg)
        
        if master.playTestSound is True:
            master.playMIDI("music/midi/sightReading/" + self.testImage)

# Intervals tutorial
class IntervalsTutorialPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        intervalExampleImage = Image.open("images/exampleIntervals.png")  # Hyacinth, CC BY-SA 3.0, via Wikimedia Commons+
        self.intervalExampleImg = ImageTk.PhotoImage(intervalExampleImage)
        self.intervalExampleImageLabel = Label(self, image = self.intervalExampleImg)
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
        ttk.Frame.__init__(self, master)
        
        # Question counter
        self.questionCounter = 0
        
        # Add score counter
        self.score = 0
        self.scoreCounter = ttk.Label(self, text = "Score: " + str(self.score) + "/" + str(self.questionCounter), font = ("TkDefaultFont", 32))
        self.scoreCounter.pack()
        
        self.imageFolderOptions = listdir("images/intervals/harmonic")
        
        # Get rid of the .DS_Store file as it crashes code
        if platform == "darwin":  # if the operating system is a Mac
            self.imageFolderOptions.remove('.DS_Store')
        
        self.selectRandomImage("intervals/harmonic")      
        
        intervalImage = Image.open("images/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
        self.intervalImg = ImageTk.PhotoImage(intervalImage)
        self.harmonicIntervalImageLabel = Label(self, image = self.intervalImg)
        self.harmonicIntervalImageLabel.pack()
        
        if master.playTestSound is True:
            master.playMIDI("music/midi/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
        
        self.p5Button = ttk.Button(self, text = "P5", command = lambda: self.buttonClicked(master, "P5"))
        self.p5Button.pack()
        
        self.octaveButton = ttk.Button(self, text = "Octave", command = lambda: self.buttonClicked(master, "Octave"))
        self.octaveButton.pack()
    
    def selectRandomImage(self, testTopic):
        self.imageFolder = choice(self.imageFolderOptions)
        imagePitchOptions = listdir("images/" + testTopic + "/" + self.imageFolder)
        self.testImage = choice(imagePitchOptions)
    
    def buttonClicked(self, master, selectedButton):
        self.questionCounter += 1
        
        if selectedButton == self.imageFolder:
            self.score += 1
            self.scoreCounter.config(text = "Score: " + str(self.score) + "/" + str(self.questionCounter))
        
        self.selectRandomImage("intervals/harmonic")
        
        newImage = Image.open("images/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
        self.newImg = ImageTk.PhotoImage(newImage)
        self.harmonicIntervalImageLabel.configure(image = self.newImg)
        
        if master.playTestSound is True:
            master.playMIDI("music/midi/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
            
# List of all the songs users can practice along to
class MusicSelectorPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        for song in range(master.dfRange):
            ttk.Button(self, text = master.songNameList[song], command = lambda i=song: self.playSong(master, i)).pack()
        
    def playSong(self, master, chosenSong):
        global selectedSong, songFile  # Only global part until I can find a way to bring the variables into another page
        
        folders = master.df.loc[:, "Folder"]
        folderList = folders.tolist()
        
        songFile = folderList[chosenSong]
        selectedSong = chosenSong
        
        app.switchPage(MusicPlayerPage)
        
# The music player
class MusicPlayerPage(ttk.Frame):
    def __init__(self, master):        
        # Credit for play/pause buttons: © 2014 Andreas Kainz & Uri Herrera & Andrew Lake & Marco Martin & Harald Sitter & Jonathan Riddell & Ken Vermette & Aleix Pol & David Faure & Albert Vaca & Luca Beltrame & Gleb Popov & Nuno Pinheiro & Alex Richardson & Jan Grulich & Bernhard Landauer & Heiko Becker & Volker Krause & David Rosca & Phil Schaf / KDE
        ttk.Frame.__init__(self, master)
        
        # Call the corresponding song data
        chosenSongTitle = master.songNameList[selectedSong]
        chosenSongArtist = master.songArtistList[selectedSong]
        chosenSongAlbum = master.songAlbumList[selectedSong]
        albumFile = master.albumCoverList[selectedSong]
        
        # Create the song information
        albumCover = Image.open("images/albumCovers/" + albumFile)
        self.albumCoverImg = ImageTk.PhotoImage(albumCover)
        self.albumCoverLabel = Label(self, image = self.albumCoverImg)
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
        
        # Create the volume sliders for the mixer tracks
        # Bass slider
        self.bassSlider = Scale(self, from_ = 100, to = 0, command = self.bassVolume)
        if master.appTheme == "equilux":
            self.bassSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.bassSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.bassSlider.set(100)
        self.bassSlider.grid(row = 9, column = 0)
        
        self.bassSliderLabel = ttk.Label(self, text = "Bass", wraplength = 1, justify = CENTER)
        self.bassSliderLabel.grid(row = 9, column = 1, sticky = W)
        
        # Drums slider
        self.drumsSlider = Scale(self, from_ = 100, to = 0, command = self.drumsVolume)
        if master.appTheme == "equilux":
            self.drumsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.drumsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.drumsSlider.set(100)
        self.drumsSlider.grid(row = 9, column = 2)
        
        self.drumsSliderLabel = ttk.Label(self, text = "Drums", wraplength = 1, justify = CENTER)
        self.drumsSliderLabel.grid(row = 9, column = 3, sticky = W)
        
        # Other slider
        self.otherSlider = Scale(self, from_ = 100, to = 0, command = self.otherVolume)
        if master.appTheme == "equilux":
            self.otherSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.otherSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.otherSlider.set(100)
        self.otherSlider.grid(row = 9, column = 4)
        
        self.otherSliderLabel = ttk.Label(self, text = "Other", wraplength = 1, justify = CENTER)
        self.otherSliderLabel.grid(row = 9, column = 5, sticky = W)
        
        # Piano slider
        self.pianoSlider = Scale(self, from_ = 100, to = 0, command = self.pianoVolume)
        if master.appTheme == "equilux":
            self.pianoSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.pianoSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.pianoSlider.set(100)
        self.pianoSlider.grid(row = 9, column = 6)
        
        self.pianoSliderLabel = ttk.Label(self, text = "Piano", wraplength = 1, justify = CENTER)
        self.pianoSliderLabel.grid(row = 9, column = 7, sticky = W)
        
        # Vocals slider
        self.vocalsSlider = Scale(self, from_ = 100, to = 0, command = self.vocalVolume)
        if master.appTheme == "equilux":
            self.vocalsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.vocalsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.vocalsSlider.set(100)
        self.vocalsSlider.grid(row = 9, column = 8)
        
        self.vocalsSliderLabel = ttk.Label(self, text = "Vocals", wraplength = 1, justify = CENTER)
        self.vocalsSliderLabel.grid(row = 9, column = 9, sticky = W)
        
        ttk.Label(self, text = " ").grid(row = 10)  # Spacing out frame
    
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
       
    def vocalVolume(self, x):
        volume = self.vocalsSlider.get() / 100
        self.channel5.set_volume(volume)
        
# The settings page       
class SettingsPage(ttk.Frame):
    def __init__(self, master):        
        ttk.Frame.__init__(self, master)
        
        self.darkModeCheckbox = ttk.Checkbutton(self, text = "Dark Mode", command = lambda: master.changeTheme(master.appTheme))
        
        if master.appTheme == "equilux":
            self.darkModeCheckbox.state(["selected"])
        
        self.darkModeCheckbox.pack()
        
        self.playTestMusicCheckbox = ttk.Checkbutton(self, text = "Play music in tests", command = lambda: master.changePlaySoundTestVariable(master.playTestSound))
        
        if master.playTestSound is True:
            self.playTestMusicCheckbox.state(["selected"])
        
        self.playTestMusicCheckbox.pack()
        
# About page
class AboutPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        aboutText = ttk.Label(self, text = "My intended outcome is to make a Graphical User Interface (GUI) to help people learn aspects of music theory, understand some musical\nfundamentals, and practice their instruments.  A particularly innovative feature I want to include is a music player that users can customise to hear\nwhat they want. For example, vocals can be removed from a track so the user can use it like a karaoke machine. Alternatively, the bass can be\n removed from the track if the user wants to practice bass by playing along with the songs.\n\nIn the market today, some apps and programs do have these functions, only with some significant drawbacks. They are either pay-to-use, averaging NZ$8.99\n(like the ABRSM Aural Trainer app), too complicated for my age group (like the UCLA Music Theory app), or too basic to be useful (like Mussila Music). My\n program will be free to use, contain the necessary lessons that beginners can use intuitively, and contain some fun play-along features not available in other apps. ", font = ("TkDefaultFont", 20), justify = CENTER)
        aboutText.pack()
             
#############
# Main code #
#############   
if __name__ == "__main__":    
    # Initialise pygame's mixer
    mixer.pre_init(0, -16, 5, 512)
    mixer.init()
    
    # Run the app
    app = musicApp()
    app.mainloop()
