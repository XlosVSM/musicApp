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
from random import choice, randint
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
            playTestSoundStr = userSettings.loc[1, "State"]
            if playTestSoundStr == "True":
                self.playTestSound = True
            
            else:
                self.playTestSound = False
        
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
        
        # Get the data from the json files
        self.songPlayerDf = read_json("songInfo.json")
        self.terminologyDf = read_json("terminology.json")
    
        # Create lists of the data from the JSON file to speed up the program     
        self.songNameList = self.songPlayerDf.loc[:, "Song Name"].tolist()
        self.songArtistList = self.songPlayerDf.loc[:, "Artist"].tolist()
        self.songAlbumList = self.songPlayerDf.loc[:, "Album"].tolist()
        self.albumCoverList = self.songPlayerDf.loc[:, "Album Cover"].tolist()
        self.terminologyTerm = self.terminologyDf.loc[:, "Term"].tolist()
        self.terminologyDescription = self.terminologyDf.loc[:, "Description"].tolist()
        
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

        # Home cascade
        menuBar.addMenuBar(
            "Home", commands = [
                ("Home", lambda: self.switchPage(StartPage))
            ]
        )

        # Intervals cascade
        menuBar.addMenuBar(
            "Intervals", commands = [
                ("Tutorial", lambda: self.switchPage(IntervalsTutorialPage)),
                ("Harmonic", lambda: self.switchPage(HarmonicIntervalsTest)),
                ("Melodic", lambda: self.switchPage(MelodicIntervalsTest))
            ]
        )

        # Sight reading cascade
        menuBar.addMenuBar(
            "Sight Reading", commands = [
                ("Tutorial", lambda: self.switchPage(SightReadingTutorialPage)),
                ("Test", lambda: self.switchPage(SightReadingTest))
            ]
        )
    
        # Terminology cascade
        menuBar.addMenuBar(
            "Terminology", commands = [
                ("Tutorial", lambda: self.switchPage(TerminologyTutorialPage)),
                ("Flash Cards", lambda: self.switchPage(TerminologyFlashCardsPage))
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
                ("Settings", lambda: self.switchPage(SettingsPage)),
                ("About", lambda: self.switchPage(AboutPage))
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
        if currentState == False:
            self.playTestSound = True
            
        else:
            self.playTestSound = False
        
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
        imageFolderOptions = listdir(f"images/{testTopic}")
        # Remove the .DS_Store if it exists in the list
        try:
            imageFolderOptions.remove(".DS_Store")
        
        except ValueError:
            pass

        imageFolder = choice(imageFolderOptions)

        clefOptions = listdir(f"images/{testTopic}/{imageFolder}")
        try:
            clefOptions.remove(".DS_Store")
        
        except ValueError:
            pass

        clef = choice(clefOptions)

        testImageOptions = listdir(f"images/{testTopic}/{imageFolder}/{clef}")
        try:
            testImageOptions.remove(".DS_Store")
        
        except ValueError:
            pass

        testImage = choice(testImageOptions)

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

# Make bigger
# Put about page back
# Link sight reading button to test
# Make buttons bigger
# Change shade of buttons in test
# Put a brief explanation for instrument practice

# The opening page
class StartPage(ttk.Frame):
    def __init__(self, master):       
        ttk.Frame.__init__(self, master)
        
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

        # Sub header
        self.subHeader = ttk.Label(self, text = "              Learn music the easy way \n", font = ("Helvetica", 32))
        self.subHeader.grid(row = 1, columnspan = 5, sticky = E + W)

        # Image of the treble clef
        trebleImage = Image.open("images/trebleClef.png")
        self.trebleImg = ImageTk.PhotoImage(trebleImage)
        self.trebleImageLabel = Label(self, image = self.trebleImg)
        self.trebleImageLabel.grid(rowspan = 3, column = 0)
        
        # Buttons which will lead to the relevant page for every section
        self.intervalsButton = Button(self, text = "Intervals", command = lambda: master.switchPage(IntervalsTutorialPage))
        self.intervalsButton.grid(row = 2, column = 1, sticky = N + S + E + W)

        self.sightReadingButton = Button(self, text = "\n\n\n  Sight Reading \n\n\n", command = lambda: master.switchPage(SightReadingTutorialPage))
        self.sightReadingButton.grid(row = 2, column = 2, sticky = N + S + E + W)
        
        self.terminologyButton = Button(self, text = "  Terminology   ", command = lambda: master.switchPage(TerminologyFlashCardsPage))
        self.terminologyButton.grid(row = 3, column = 1, sticky = N + S + E + W)
        
        self.instrumentPracticeButton = Button(self, text = "\n\nInstrument\nPractice\n\n", command =  lambda: master.switchPage(MusicSelectorPage))
        self.instrumentPracticeButton.grid(row = 3, column = 2, sticky = N + S + E + W)

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
        informationLabel = ttk.Label(self, text = '''\nIntervals is the distance between two notes. Above is a picture showing what all the\nintervals will look like at the tonic of middle C. The way to tell what the interval is by\ncounting how many lines and gaps there are between the notes starting on the first note.\nFor example, a perfect fourth would have 4 lines and gaps in between it.\n''', font = ("TkDefaultFont", 20), justify =  CENTER)
        informationLabel.pack()
        
        # Button to the harmonic interval test
        harmonicIntervalTestButton = Button(self, text = "Harmonic Interval Test", command = lambda: master.switchPage(HarmonicIntervalsTest), height = 8)
        harmonicIntervalTestButton.pack(side = LEFT, fill = 'x', padx = 128)
        
        # Button to the melodic interval test
        melodicIntervalTestButton = Button(self, text = "Melodic Interval Test", command = lambda: master.switchPage(MelodicIntervalsTest), height = 8)
        melodicIntervalTestButton.pack(side = RIGHT, fill = 'x', padx = 128)

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
        
        self.fileValues = master.selectRandomImage("intervals/harmonic")
        
        # Create the image of a random interval
        intervalImage = Image.open(f"images/intervals/harmonic/{self.fileValues[0]}/{self.fileValues[1]}/{self.fileValues[2]}")
        self.intervalImg = ImageTk.PhotoImage(intervalImage)
        self.harmonicIntervalImageLabel = Label(self, image = self.intervalImg)
        self.harmonicIntervalImageLabel.pack()

        # Question to help explain to the user what to do
        ttk.Label(self, text = "\nIs this interval a Perfect Fifth (P5) or an Octave?\n", font = ("TkDefaultTheme", 32)).pack()
        
        # Create buttons of the intervals being tested
        self.p5Button = Button(self, text = "Perfect\nFifth", command = lambda: self.buttonClicked(master, "P5"), height = 8, width = 8)
        self.p5Button.pack(side = LEFT, fill = 'x', padx = 128)
        
        self.octaveButton = Button(self, text = "Octave", command = lambda: self.buttonClicked(master, "Octave"), height = 8, width = 8)
        self.octaveButton.pack(side = RIGHT, fill = 'x', padx = 128)

        # Maybe add a blank line

        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"intervals/harmonic/{self.fileValues[0]}/{self.fileValues[2]}")
    
    def buttonClicked(self, master, selectedButton):
        # Update the score counter
        self.questionCounter += 1
        
        if selectedButton == self.fileValues[0]:
            self.score += 1
        
        self.scoreCounter.config(text = "Score: " + str(self.score) + "/" + str(self.questionCounter))
        
        self.fileValues = master.selectRandomImage("intervals/harmonic")  # Get a new random interval
        
        # Update the image
        newImage = Image.open(f"images/intervals/harmonic/{self.fileValues[0]}/{self.fileValues[1]}/{self.fileValues[2]}")
        self.newImg = ImageTk.PhotoImage(newImage)
        self.harmonicIntervalImageLabel.configure(image = self.newImg)
        
        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"intervals/harmonic/{self.fileValues[0]}/{self.fileValues[2]}")

# Melodic intervals test
class MelodicIntervalsTest(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Question counter
        self.questionCounter = 0
        
        # Add score counter
        self.score = 0
        self.scoreCounter = ttk.Label(self, text = f"Score: {str(self.score)}/{str(self.questionCounter)}", font = ("TkDefaultFont, 32"))
        self.scoreCounter.pack()
        
        self.fileValues = master.selectRandomImage("intervals/melodic")

        # Create the image of a random interval
        intervalImage = Image.open(f"images/intervals/melodic/{self.fileValues[0]}/{self.fileValues[1]}/{self.fileValues[2]}")
        self.intervalImg = ImageTk.PhotoImage(intervalImage)
        self.harmonicIntervalImageLabel = Label(self, image = self.intervalImg)
        self.harmonicIntervalImageLabel.pack()

        # Question to help explain to the user what to do
        ttk.Label(self, text = "\nIs this interval a Perfect Fifth (P5) or an Octave?\n", font = ("TkDefaultTheme", 32)).pack()
        
        # Create buttons of the intervals being tested
        self.p5Button = Button(self, text = "Perfect\nFifth", command = lambda: self.buttonClicked(master, "P5"), height = 8, width = 8)
        self.p5Button.pack(side = LEFT, fill = 'x', padx = 128)
        
        self.octaveButton = Button(self, text = "Octave", command = lambda: self.buttonClicked(master, "Octave"), height = 8, width = 8)
        self.octaveButton.pack(side = RIGHT, fill = 'x', padx = 128)

        # Maybe add a blank line

        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"intervals/melodic/{self.fileValues[0]}/{self.fileValues[2]}")
    
    def buttonClicked(self, master, selectedButton):
        # Update the score counter
        self.questionCounter += 1
        
        if selectedButton == self.fileValues[0]:
            self.score += 1
        
        self.scoreCounter.config(text = "Score: " + str(self.score) + "/" + str(self.questionCounter))
        
        self.fileValues = master.selectRandomImage("intervals/melodic")  # Get a new random interval
        
        # Update the image
        newImage = Image.open(f"images/intervals/melodic/{self.fileValues[0]}/{self.fileValues[1]}/{self.fileValues[2]}")
        self.newImg = ImageTk.PhotoImage(newImage)
        self.harmonicIntervalImageLabel.configure(image = self.newImg)
        
        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"intervals/melodic/{self.fileValues[0]}/{self.fileValues[2]}")

# Sight reading tutorial
class SightReadingTutorialPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        ttk.Label(self, text = "shut up meg").pack()

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
        
        self.fileValues = master.selectRandomImage("sightReading")
        
        # Create the image of a random note
        sightReadingImage = Image.open(f"images/sightReading/{self.fileValues[0]}/{self.fileValues[1]}/{self.fileValues[2]}")
        self.sightReadingImg = ImageTk.PhotoImage(sightReadingImage)
        self.sightReadingImageLabel = Label(self, image = self.sightReadingImg)
        self.sightReadingImageLabel.pack()

        # Question to help explain to the user what to do
        ttk.Label(self, text = "\nSelect the note shown in the picture above\n", font = ("TkDefaultTheme", 32)).pack()
        
        # Creating the buttons for all the notes
        self.aFlatButton = Button(self, text = "Ab", command = lambda: self.buttonClicked(master, "Ab", "sightReading"), height = 5, width = 5)
        self.aFlatButton.pack(side = LEFT)
        
        self.aButton = Button(self, text = "A", command = lambda: self.buttonClicked(master, "A", "sightReading"), height = 5, width = 5)
        self.aButton.pack(side = LEFT)
        
        self.bFlatButton = Button(self, text = "Bb", command = lambda: self.buttonClicked(master, "Bb", "sightReading"), height = 5, width = 5)
        self.bFlatButton.pack(side = LEFT)
        
        self.bButton = Button(self, text = "B", command = lambda: self.buttonClicked(master, "B", "sightReading"), height = 5, width = 5)
        self.bButton.pack(side = LEFT)
        
        self.cButton = Button(self, text = "C", command = lambda: self.buttonClicked(master, "C", "sightReading"), height = 5, width = 5)
        self.cButton.pack(side = LEFT)
        
        self.cSharpButton = Button(self, text = "C#", command = lambda: self.buttonClicked(master, "C#", "sightReading"), height = 5, width = 5)
        self.cSharpButton.pack(side = LEFT)
        
        self.dButton = Button(self, text = "D", command = lambda: self.buttonClicked(master, "D", "sightReading"), height = 5, width = 5)
        self.dButton.pack(side = LEFT)
        
        self.eFlatButton = Button(self, text = "Eb", command = lambda: self.buttonClicked(master, "Eb", "sightReading"), height = 5, width = 5)
        self.eFlatButton.pack(side = LEFT)
        
        self.eButton = Button(self, text = "E", command = lambda: self.buttonClicked(master, "E", "sightReading"), height = 5, width = 5)
        self.eButton.pack(side = LEFT)
        
        self.fButton = Button(self, text = "F", command = lambda: self.buttonClicked(master, "F", "sightReading"), height = 5, width = 5)
        self.fButton.pack(side = LEFT)
        
        self.fSharpButton = Button(self, text = "F#", command = lambda: self.buttonClicked(master, "F#", "sightReading"), height = 5, width = 5)
        self.fSharpButton.pack(side = LEFT)
        
        self.gButton = Button(self, text = "G", command = lambda: self.buttonClicked(master, "G", "sightReading"), height = 5, width = 5)
        self.gButton.pack(side = LEFT)
        
        # Play the corresponding MIDI file if the user has selected the option
        if master.playTestSound is True:
            master.playMIDI(f"sightReading/{self.fileValues[0]}/{self.fileValues[2]}")
            
    def buttonClicked(self, master, selectedButton, testTopic):
        self.questionCounter += 1
        
        if selectedButton == self.fileValues[0]:
            self.score += 1
            
        self.scoreCounter.config(text = f"Score: {str(self.score)}/{str(self.questionCounter)}")
        
        newFileValues = master.selectRandomImage("sightReading")
        
        newImage = Image.open(f"images/sightReading/{newFileValues[0]}/{newFileValues[1]}/{newFileValues[2]}")
        self.newImg = ImageTk.PhotoImage(newImage)
        self.sightReadingImageLabel.configure(image = self.newImg)
        
        if master.playTestSound is True:
            master.playMIDI(f"sightReading/{newFileValues[0]}/{newFileValues[2]}")

# Terminology tutorial page
class TerminologyTutorialPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        ttk.Label(self, text = "Supercalifragilisticxpalidocious").pack()

# Terminology flash cards page
class TerminologyFlashCardsPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        chosenTerm = randint(0,1)
        self.term = master.terminologyTerm[chosenTerm]
        self.description = master.terminologyDescription[chosenTerm]
        
        self.currentState = "term"

        # Music theory terms at https://gb.abrsm.org/media/64638/music-theory-terms-and-signs-for-grades-1-5-from-2020.pdf
        flashCard = Canvas(self, width = 540, height = 540, bg = "white")
        flashCard.pack(expand = YES, fill = BOTH)
        self.termFlashCard = Label(self, text = self.term, font = ("TkDefaultTheme", 32), bg = "white", fg = "black")
        self.termFlashCard.pack()
        flashCard.create_window(270, 270, window = self.termFlashCard)

        # Pick a new card button
        self.newCardButton = Button(self, text = "  Pick a new card  ", command = lambda: self.newFlashCard(master), font = ("TkDefaultTheme", 32))
        self.newCardButton.pack()

        # Flip card
        self.flipButton = Button(self, text = "Flip the flash card", command = self.flipFlashCard, font = ("TkDefaultTheme", 32))
        self.flipButton.pack()

    def newFlashCard(self, master):
        newChosenTerm = randint(0,1)
        self.term = master.terminologyTerm[newChosenTerm]
        self.description = master.terminologyDescription[newChosenTerm]

        self.termFlashCard.config(text = self.term)
    
    def flipFlashCard(self):
        if self.currentState == "term":
            self.termFlashCard.config(text = self.description)
            self.currentState = "description"
        
        else:
            self.termFlashCard.config(text = self.term)
            self.currentState = "term"

# List of all the songs users can practice along to
class MusicSelectorPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        ttk.Label(self, text = "\n Choose which song you would like to practice \n", font = ("TkDefaultTheme", 24)).pack()

        # Create a button for all the song options
        for song in range(len(master.songPlayerDf)):
            Button(self, text = master.songNameList[song], command = lambda i=song: self.playSong(master, i), font = ("TkDefaultTheme", 32), height = 4).pack()
        
    def playSong(self, master, chosenSong):    
        folders = master.songPlayerDf.loc[:, "Folder"]
        folderList = folders.tolist()
        
        MusicPlayerPage.songFile = folderList[chosenSong]
        MusicPlayerPage.selectedSong = chosenSong
        
        master.switchPage(MusicPlayerPage)
        
# The music player
class MusicPlayerPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Add a back to music selector button
        
        # Call the corresponding song data
        chosenSongTitle = master.songNameList[self.selectedSong]
        chosenSongTitle.strip()
        chosenSongArtist = master.songArtistList[self.selectedSong]
        chosenSongAlbum = master.songAlbumList[self.selectedSong]
        albumFile = master.albumCoverList[self.selectedSong]
        
        # Create the song information
        albumCover = Image.open("images/albumCovers/" + albumFile)
        self.albumCoverImg = ImageTk.PhotoImage(albumCover)
        self.albumCoverLabel = Label(self, image = self.albumCoverImg)
        self.albumCoverLabel.grid(rowspan = 6, columnspan = 6)
        
        songName = ttk.Label(self, text = f" Title: {chosenSongTitle.strip()} ", font = ("Helvetica", 20), justify = CENTER)
        songName.grid(row = 0, column = 6, columnspan = 3)
        
        artistName = ttk.Label(self, text = f"Artist: {chosenSongArtist} ", font = ("Helvetica", 20), justify = CENTER)
        artistName.grid(row = 2, column = 6, columnspan = 3)
        
        albumName = ttk.Label(self, text = f"Album: {chosenSongAlbum} ", font = ("Helvetica", 20), justify = CENTER)
        albumName.grid(row = 4, column = 6, columnspan = 3)
        
        # Play the song
        self.file = "music/stems/" + self.songFile
        
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
        
        # Create a label for mixers
        mixerLabel = ttk.Label(self, text = "\nMIXERS", font = ("TkDefaultTheme", 28))
        mixerLabel.grid(row = 7, columnspan = 9)

        # Create the volume sliders for the mixer tracks
        # Bass slider
        self.bassSlider = Scale(self, from_ = 100, to = 0, command = self.bassVolume)
        if master.appTheme == "equilux":
            self.bassSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.bassSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.bassSlider.set(100)
        self.bassSlider.grid(row = 8, column = 0)
        
        self.bassSliderLabel = ttk.Label(self, text = "Bass", wraplength = 1, justify = CENTER)
        self.bassSliderLabel.grid(row = 8, column = 1, sticky = W)
        
        # Drums slider
        self.drumsSlider = Scale(self, from_ = 100, to = 0, command = self.drumsVolume)
        if master.appTheme == "equilux":
            self.drumsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.drumsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.drumsSlider.set(100)
        self.drumsSlider.grid(row = 8, column = 2)
        
        self.drumsSliderLabel = ttk.Label(self, text = "Drums", wraplength = 1, justify = CENTER)
        self.drumsSliderLabel.grid(row = 8, column = 3, sticky = W)
        
        # Other slider
        self.otherSlider = Scale(self, from_ = 100, to = 0, command = self.otherVolume)
        if master.appTheme == "equilux":
            self.otherSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.otherSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.otherSlider.set(100)
        self.otherSlider.grid(row = 8, column = 4)
        
        self.otherSliderLabel = ttk.Label(self, text = "Other", wraplength = 1, justify = CENTER)
        self.otherSliderLabel.grid(row = 8, column = 5, sticky = W)
        
        # Piano slider
        self.pianoSlider = Scale(self, from_ = 100, to = 0, command = self.pianoVolume)
        if master.appTheme == "equilux":
            self.pianoSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.pianoSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.pianoSlider.set(100)
        self.pianoSlider.grid(row = 8, column = 6)
        
        self.pianoSliderLabel = ttk.Label(self, text = "Piano", wraplength = 1, justify = CENTER)
        self.pianoSliderLabel.grid(row = 8, column = 7, sticky = W)
        
        # Vocals slider
        self.vocalsSlider = Scale(self, from_ = 100, to = 0, command = self.vocalVolume)
        if master.appTheme == "equilux":
            self.vocalsSlider.config(bg = "gray33", activebackground="gray33")
            
        else:
            self.vocalsSlider.config(bg = "white", activebackground = "white", fg = "black")
        
        self.vocalsSlider.set(100)
        self.vocalsSlider.grid(row = 8, column = 8)
        
        self.vocalsSliderLabel = ttk.Label(self, text = "Vocals", wraplength = 1, justify = CENTER)
        self.vocalsSliderLabel.grid(row = 8, column = 9, sticky = W)
        
        ttk.Label(self, text = " ").grid(row = 9)  # Spacing out frame

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
        
        ttk.Label(self, text = "Music Learning App", font = ("TkDefaultTheme", 64)).pack()
        ttk.Label(self, text = 'by Matthew McDermott', font = ("TkDefaultTheme", 24)).pack()
        ttk.Label(self, text = "\nPURPOSE: A digital technology NCEA Level 3 project. This is a music learning app for intermediate level music students.\n", font = ("TkDefaultTheme", 20)).pack()
        ttk.Label(self, text = "My intended outcome is to make a Graphical User Interface (GUI) to help people learn aspects of music theory, understand some musical\nfundamentals, and practice their instruments.  A particularly innovative feature I want to include is a music player that users can customise to hear\nwhat they want. For example, vocals can be removed from a track so the user can use it like a karaoke machine. Alternatively, the bass can be\n removed from the track if the user wants to practice bass by playing along with the songs.\n\nIn the market today, some apps and programs do have these functions, only with some significant drawbacks. They are either pay-to-use, averaging NZ$8.99\n(like the ABRSM Aural Trainer app), too complicated for my age group (like the UCLA Music Theory app), or too basic to be useful (like Mussila Music). My\n program will be free to use, contain the necessary lessons that beginners can use intuitively, and contain some fun play-along features not available in other apps. \n", font = ("TkDefaultFont", 20), justify = CENTER).pack()
        ttk.Label(self, text = "\n\nCopyright 2022\n", font = ("TkDefaultTheme", 24)).pack()
                     
#############
# Main code #
#############   
if __name__ == "__main__":    
    # Initialise pygame's mixer
    mixer.pre_init(0, -16, 5, 512)
    mixer.init()
    
    musicApp().mainloop()  # Run the app
