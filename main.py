##### Imports #####
# GUI Creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk

# Music
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Stop pygame's welcome message popping up in console
from pygame import mixer

'''''''''
WIDTH = 606
HEIGHT = 457
'''''''''

##### Classes #####
class musicApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        # Style the code
        self.title("Music App")
        self.geometry("606x457")
        self.style = ThemedStyle(self)
        self.style.set_theme(appTheme)
        
        # Open on the starting page
        self._frame = None
        self.switchFrame(StartPage)
    
    def addMenu(self, menuName, commands):
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)        
    
    def switchFrame(self, frameClass):
        # Stop music from playing
        for x in range(5):
            mixer.Channel(x).stop()
        
        newFrame = frameClass(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = newFrame
        self._frame.pack()
    
    def changeTheme(self, theme):
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

class MenuBar():
    def __init__(self, parent):
        self.menuBar = Menu(parent)
        self.create()
        
    def create(self):
        app.config(menu = self.menuBar)
        
    def addMenu(self, menuName, commands):
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)

class StartPage(ttk.Frame):
    def __init__(self, master):
        global bassImg, trebleImg # Images must be global so they can be seen
        
        ttk.Frame.__init__(self, master)
        self.grid(sticky = N + S + E + W)
        
        # Configure the grid's columns
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(4, weight = 1)
        # self.grid_columnconfigure(0, weight = 7)
        # self.grid_columnconfigure(2, weight = 1)
        # self.grid_columnconfigure(3, weight = 4)
        # self.grid_columnconfigure(4, weight = 3)
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
        
        self.instrumentPracticeButton = ttk.Button(self, text = "\n\nInstrument\nPractice\n\n", command =  lambda: master.switchFrame(MusicPlayerPage))
        self.instrumentPracticeButton.grid(row = 3, column = 2, sticky = N + S + E + W)
        '''
        bassImage = Image.open("images/bassClef.png")
        bassImageResized = bassImage.resize((135,373))
        bassImg = ImageTk.PhotoImage(bassImageResized)
        self.bassImageLabel = Label(self, image = bassImg)
        self.bassImageLabel.grid(rowspan = 4, column = 4)
        '''
        
class MusicPlayerPage(ttk.Frame):
    def __init__(self, master):
        global channel5, vocalsSlider
        
        ttk.Frame.__init__(self, master)
        
        channel1 = mixer.Channel(0)
        channel1Sound = mixer.Sound("music/stems/TameImpala_Elephant/bass.wav")
        channel1.play(channel1Sound)

        channel2 = mixer.Channel(1)
        channel2Sound = mixer.Sound("music/stems/TameImpala_Elephant/drums.wav")
        channel2.play(channel2Sound)

        channel3 = mixer.Channel(2)
        channel3Sound = mixer.Sound("music/stems/TameImpala_Elephant/other.wav")
        channel3.play(channel3Sound)

        channel4 = mixer.Channel(3)
        channel4Sound = mixer.Sound("music/stems/TameImpala_Elephant/piano.wav")
        channel4.play(channel4Sound)

        channel5 = mixer.Channel(4)
        channel5Sound = mixer.Sound("music/stems/TameImpala_Elephant/vocals.wav")
        channel5.play(channel5Sound)
        
        vocalsSlider = Scale(self, from_ = 100, to = 0, command = vocalVolume)
        vocalsSlider.set(100)
        vocalsSlider.pack()
            
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
        
        ttk.Button(self, text = "Home", command = lambda: master.switchFrame(StartPage)).pack()
        
##### Definitions ######      
def firstTheme():
    from darkdetect import isDark
    
    if isDark() == True:
        appTheme = "equilux"
    
    else:
        appTheme = "yaru"
        
    # Create a file so the code uses the theme next time the user runs the code
    with open('theme.txt', 'w') as i:
        i.write(appTheme)
    
    return appTheme

def menuPass():
    pass

def createMenuBar():
    menuBar = MenuBar(app)
    
    # Instrument roles cascade
    menuBar.addMenu(
        "Instrument Roles", commands = [
            ("Rock Band", menuPass, True)
        ],
    )

    # Sight reading cascade
    menuBar.addMenu(
        "Sight Reading", commands = [
            ("Tutorial", menuPass, True),
            ("Test", menuPass, True)
        ]
    )
    
    # Intervals cascade
    menuBar.addMenu(
        "Intervals", commands = [
            ("Tutorial", menuPass, True),
            ("Melodic", menuPass, True),
            ("Harmonic", menuPass, True)
        ]
    )
    
    # Chords cascade
    menuBar.addMenu(
        "Chords", commands = [
            ("Tutorial", menuPass, True),
            ("Chord Quality", menuPass, True),
            ("Cadences", menuPass, True),
        ]
    )
    
    # Terminology cascade
    menuBar.addMenu(
        "Terminology", commands = [
            ("Tutorial", menuPass, True),
            ("Flash Cards", menuPass, True)
        ]
    )
    
    # Instrument practice cascade
    menuBar.addMenu(
        "Instrument Practice", commands = [
            ("Choose Song", lambda: app.switchFrame(MusicPlayerPage), True)
        ]
    )
        
    # Preferences cascade
    menuBar.addMenu(
        "Preferences", commands = [
            ("Settings", lambda: app.switchFrame(SettingsPage), True)
        ]
    )

def vocalVolume(x):
    volume = vocalsSlider.get()/100
    channel5.set_volume(volume)

##### Main code #####    
if __name__ == "__main__":
    # Try getting the user's preferred theme
    try:
        with open('theme.txt') as i:
            appTheme = i.readline()
    
    # First time use
    except FileNotFoundError:
        appTheme = firstTheme()
    
    mixer.pre_init(0, -16, 5, 512)
    mixer.init()
    
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
