##### Imports #####
# GUI Creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle

# Music
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

##### Classes #####
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
        self.switchFrame(StartPage)
    
    def addMenu(self, menuName, commands):
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)        
    
    def switchFrame(self, frameClass):
        global musicStop
        
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
        ttk.Frame.__init__(self, master)
        
        ttk.Label(self, text = "TEST").pack()
        
        ttk.Button(self, text = "Settings", command = lambda: master.switchFrame(SettingsPage)).pack()
        
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
    
def testPass():
    pass

def createMenuBar():
    menuBar = MenuBar(app)
    
    # Instrument roles cascade
    menuBar.addMenu(
        "Instrument Roles", commands = [
            ("Rock Band", testPass, True)
        ],
    )

    # Sight reading cascade
    menuBar.addMenu(
        "Sight Reading", commands = [
            ("Tutorial", testPass, True),
            ("Test", testPass, True)
        ]
    )
    
    # Intervals cascade
    menuBar.addMenu(
        "Intervals", commands = [
            ("Tutorial", testPass, True),
            ("Melodic", testPass, True),
            ("Harmonic", testPass, True)
        ]
    )
    
    # Chords cascade
    menuBar.addMenu(
        "Chords", commands = [
            ("Tutorial", testPass, True),
            ("Chord Quality", testPass, True),
            ("Cadences", testPass, True),
        ]
    )
    
    # Terminology cascade
    menuBar.addMenu(
        "Terminology", commands = [
            ("Tutorial", testPass, True),
            ("Flash Cards", testPass, True)
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

##### Main code #####    
if __name__ == "__main__":
    # Try getting the user's preferred theme
    try:
        with open('theme.txt') as f:
            appTheme = f.readline()
    
    # First time use
    except FileNotFoundError:
        appTheme = firstTheme()
    
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
