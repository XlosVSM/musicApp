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
        
        except FileNotFoundError:  # If it is the user's first time running the code or preferences is missing
            self.appTheme = self.setDefaultTheme()
            self.playTestSound = True
            
            # Create the JSON file to store preferences
            data = [
                ['App Theme', self.appTheme],
                ['Play Music', 'True']
            ]
            
            DataFrame(data, columns = ['Variable', 'State']).to_json('preferences.json')
        
        self.style = ThemedStyle(self)
        try:
            self.style.set_theme(self.appTheme)
        
        # If theme.txt is tampered with, it will delete the file and rewrite it
        except TclError:
            self.appTheme = self.setDefaultTheme()
            self.style.set_theme(self.appTheme)
        
        # Get the song data
        self.songPlayerDf = read_json("songInfo.json")
    
        # Create lists of the data from the JSON file to speed up the program     
        self.songNameList = self.songPlayerDf.loc[:, "Song Name"].tolist()
        self.songArtistList = self.songPlayerDf.loc[:, "Artist"].tolist()
        self.songAlbumList = self.songPlayerDf.loc[:, "Album"].tolist()
        self.albumCoverList = self.songPlayerDf.loc[:, "Album Cover"].tolist()
        
        self.createMenuBar()
        
        # Open on the starting page
        self._frame = None
        self.switchPage(StartPage)
    
    def setDefaultTheme(self): 
        if isDark() is True:  # isDark() checks if the user's device has their default theme as dark or light
            appTheme = "equilux"  # equilux is the dark theme
    
        else:
            appTheme = "yaru"  # yaru is the light theme
        
        return appTheme
    
    def null(self):  # Pass for the menu bar as you have to put a definition in
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
                ("Choose Song", lambda: self.switchPage(MusicSelectorPage))
            ]
        )
        
        # Preferences cascade
        menuBar.addMenuBar(
            "Preferences", commands = [
                ("Settings", lambda: self.switchPage(SettingsPage))
            ]
        )
            
    def switchPage(self, frameClass):  # Switch between pages
        # Stop music from playing
        for mixerChannel in range(5):
            mixer.Channel(mixerChannel).stop()
        
        # Change the page/frame
        newFrame = frameClass(self)
        
        if self._frame is not None:
            self._frame.destroy()
            
        self._frame = newFrame
        self._frame.pack()

    def changeTheme(self, currentState):
        if currentState == "equilux":
            newState = "yaru"
        
        else:
            newState = "equilux"
        
        self.style.theme_use(newState)
        self.appTheme = newState
        
        # Update the JSON file
        data = [
            ['App Theme', self.appTheme],
            ['Play Music', str(self.playTestSound)]
        ]
        
        DataFrame(data, columns = ['Variable', 'State']).to_json('preferences.json')
    
    def changePlaySoundTestVariable(self, currentState):
        if currentState == True:
            self.playTestSound = False
            
        else:
            self.playTestSound = True
        
        # Update the JSON file
        data = [
            ['App Theme', self.appTheme],
            ['Play Music', str(self.playTestSound)]
        ]
        
        DataFrame(data, columns = ['Variable', 'State']).to_json('preferences.json')
    
    def playMIDI(self, selectedMIDIFile):  # Play the MIDI files used in the tests   
        midiFileLocation = "music/midi/" + selectedMIDIFile
        midiFile = midiFileLocation.replace('.png', '.mid')
        
        mixer.music.load(midiFile)
        mixer.music.play()
        
    def selectRandomImage(self, testTopic):
        imageFolder = choice(listdir(f"images/{testTopic}"))
        clef = choice(listdir(f"images/{testTopic}/{imageFolder}"))
        testImage = choice(listdir(f"images/{testTopic}/{imageFolder}/{clef}"))
        
        return imageFolder, clef, testImage
    
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
        
        # Title
        self.header = ttk.Label(self, text = " Music Learning App ", font = ("Helvetica", 64))
        self.header.grid(row = 0, columnspan = 5, sticky = E + W)
        
        # Image of the treble clef
        trebleImage = Image.open("images/trebleClef.png")
        self.trebleImg = ImageTk.PhotoImage(trebleImage)
        self.trebleImageLabel = Label(self, image = self.trebleImg)
        self.trebleImageLabel.grid(rowspan = 4, column = 0)
        
        # Buttons which will lead to the relevant page for every section
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
        self.scoreCounter = ttk.Label(self, text = f"Score: {str(self.score)}/{str(self.questionCounter)}", font = ("TkDefaultFont", 32))
        self.scoreCounter.pack()
        
        fileValues = master.selectRandomImage("sightReading")
        
        # Create the image of a random note
        sightReadingImage = Image.open(f"images/sightReading/{fileValues[0]}/{fileValues[1]}/{fileValues[2]}")
        self.sightReadingImg = ImageTk.PhotoImage(sightReadingImage)
        self.sightReadingImageLabel = Label(self, image = self.sightReadingImg)
        self.sightReadingImageLabel.pack()
        
        # Creating the buttons for all the notes
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
        
        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"sightReading/{self.testImage}")
            
    def buttonClicked(self, master, selectedButton, testTopic):
        self.questionCounter += 1
        
        if selectedButton == self.imageFolder:
            self.score += 1
            
        self.scoreCounter.config(text = f"Score: {str(self.score)}/{str(self.questionCounter)}")
        
        fileValues = master.selectRandomImage("sightReading")
        
        newImage = Image.open(f"images/sightReading/{fileValues[0]}/{fileValues[1]}/{fileValues[2]}")
        self.newImg = ImageTk.PhotoImage(newImage)
        self.sightReadingImageLabel.configure(image = self.newImg)
        
        if master.playTestSound is True:
            master.playMIDI(f"sightReading/{self.testImage}")

# Intervals tutorial
class IntervalsTutorialPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        # Show an image of examples of intervals
        intervalExampleImage = Image.open("images/exampleIntervals.png")  # Hyacinth, CC BY-SA 3.0, via Wikimedia Commons+
        self.intervalExampleImg = ImageTk.PhotoImage(intervalExampleImage)
        self.intervalExampleImageLabel = Label(self, image = self.intervalExampleImg)
        self.intervalExampleImageLabel.pack()
        
        # Give an explanation on intervals
        informationLabel = ttk.Label(self, text = '''Intervals is the distance between two notes. Above is a picture showing what all the\nintervals will look like at the tonic of middle C. The way to tell what the interval is by\ncounting how many lines and gaps there are between the notes starting on the first note.\nFor example, a perfect fourth would have 4 lines and gaps in between it.\n''', font = ("TkDefaultFont", 20), justify =  CENTER)
        informationLabel.pack()
        
        # Button to the harmonic interval test
        harmonicIntervalTestButton = ttk.Button(self, text = "Harmonic Interval Test", command = lambda: master.switchPage(HarmonicIntervalsTest))
        harmonicIntervalTestButton.pack()
        
        # Button to the melodic interval test
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
        self.scoreCounter = ttk.Label(self, text = f"Score: {str(self.score)}/{str(self.questionCounter)}", font = ("TkDefaultFont, 32"))
        self.scoreCounter.pack()
        
        fileValues = master.selectRandomImage("intervals/harmonic")      
        
        # Create the image of a random interval
        intervalImage = Image.open(f"images/intervals/harmonic/{fileValues[0]}/{fileValues[1]}/{fileValues[2]}")
        self.intervalImg = ImageTk.PhotoImage(intervalImage)
        self.harmonicIntervalImageLabel = Label(self, image = self.intervalImg)
        self.harmonicIntervalImageLabel.pack()
        
        # Create buttons of the intervals being tested
        self.p5Button = ttk.Button(self, text = "P5", command = lambda: self.buttonClicked(master, "P5"))
        self.p5Button.pack()
        
        self.octaveButton = ttk.Button(self, text = "Octave", command = lambda: self.buttonClicked(master, "Octave"))
        self.octaveButton.pack()
        
        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI("music/midi/intervals/harmonic/" + self.imageFolder + "/" + self.testImage)
    
    def buttonClicked(self, master, selectedButton):
        # Update the score counter
        self.questionCounter += 1
        
        if selectedButton == self.imageFolder:
            self.score += 1
            self.scoreCounter.config(text = "Score: " + str(self.score) + "/" + str(self.questionCounter))
        
        fileValues = master.selectRandomImage("intervals/harmonic")
        
        # Update the image
        newImage = Image.open(f"images/intervals/harmonic/{fileValues[0]}/{fileValues[1]}/{fileValues[2]}")
        self.newImg = ImageTk.PhotoImage(newImage)
        self.harmonicIntervalImageLabel.configure(image = self.newImg)
        
        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"intervals/harmonic/{fileValues[0]}/{self.testImage}")
            
# List of all the songs users can practice along to
class MusicSelectorPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        # Create a button for all the song options
        for song in range(len(master.songPlayerDf)):
            ttk.Button(self, text = master.songNameList[song], command = lambda i=song: self.playSong(master, i)).pack()
        
    def playSong(self, master, chosenSong):
        global selectedSong, songFile  # Only global part until I can find a way to bring the variables into another page
        
        folders = master.songPlayerDf.loc[:, "Folder"]
        folderList = folders.tolist()
        
        songFile = folderList[chosenSong]
        selectedSong = chosenSong
        
        master.switchPage(MusicPlayerPage)
        
# The music player
class MusicPlayerPage(ttk.Frame):
    def __init__(self, master):
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
        
        songName = ttk.Label(self, text = f"Title: {chosenSongTitle} ", font = ("Helvetica", 20), justify = CENTER)
        songName.grid(row = 0, column = 6, columnspan = 3)
        
        artistName = ttk.Label(self, text = f"Artist: {chosenSongArtist} ", font = ("Helvetica", 20), justify = CENTER)
        artistName.grid(row = 2, column = 6, columnspan = 3)
        
        albumName = ttk.Label(self, text = f"Album: {chosenSongAlbum} ", font = ("Helvetica", 20), justify = CENTER)
        albumName.grid(row = 4, column = 6, columnspan = 3)
        
        # Play the song
        self.file = "music/stems/" + songFile
        
        # Create the channels so the user can control what parts they hear
        # Bass's channel
        self.channel1 = mixer.Channel(0)
        channel1Sound = mixer.Sound(self.file + "/bass.wav")
        self.channel1.play(channel1Sound)
        
        # Drums's channel
        self.channel2 = mixer.Channel(1)
        channel2Sound = mixer.Sound(self.file + "/drums.wav")
        self.channel2.play(channel2Sound)
        
        # Other part's channel
        self.channel3 = mixer.Channel(2)
        channel3Sound = mixer.Sound(self.file + "/other.wav")
        self.channel3.play(channel3Sound)
        
        # Piano's channel
        self.channel4 = mixer.Channel(3)
        channel4Sound = mixer.Sound(self.file + "/piano.wav")
        self.channel4.play(channel4Sound)
        
        # Vocals's channel
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
                     
#############
# Main code #
#############   
if __name__ == "__main__":    
    # Initialise pygame's mixer
    mixer.pre_init(0, -16, 5, 512)
    mixer.init()
    
    musicApp().mainloop()  # Run the app
