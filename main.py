##### Imports #####
# GUI Creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle

# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

##### Classes #####
class musicApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        # Style the code
        self.title("Music App")
        style = ThemedStyle(self)
        self.state("zoomed")
        style.set_theme(theme)
        
        # Open on the starting page
        self._frame = None
        self.switchFrame(StartPage)
    
    def addMenu(self, menuName, commands):
        menu = Menu(self.menuBar, tearoff = 0)
        
        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            
        self.menuBar.add_cascade(label = menuName, menu = menu)
    
    def switchFrame(self, frameClass):
        newFrame = frameClass(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = newFrame
        self._frame.pack()

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
        ttk.Frame.__init__(self, master)
        
        ttk.Label(self, text = "WE HERE NOW").pack()
        
        ttk.Button(self, text = "Home", command = lambda: master.switchFrame(StartPage)).pack()
        
        
##### Definitions ######      
def firstTheme():
    from darkdetect import isDark
    
    if isDark() == True:
        theme = "equilux"
    
    else:
        theme = "yaru"
        
    # Create a file so the code uses the theme next time the user runs the code
    with open('theme.txt', 'w') as i:
        i.write(theme)
    
    return theme
    
def testPass():
    pass

##### Main code #####    
if __name__ == "__main__":
    # Try getting the user's preferred theme
    try:
        with open('theme.txt') as f:
            theme = f.readline()
    
    # First time use
    except FileNotFoundError:
        theme = firstTheme()
    
    # Run the app
    try:
        app = musicApp()
    
    # If theme.txt has been altered externally
    except TclError:
        from termcolor import colored
        
        print(colored("Please delete the file theme.txt and run the code again.", "red"))
        exit()
    
    menuBar = MenuBar(app)
    
    fileMenu = menuBar.addMenu(
        "Instrument Roles", commands = [
        ("Rock Band", testPass, True)
        ],
    )

    fileMenu = menuBar.addMenu(
        "Sight Reading", commands = [
            ("Tutorial", testPass, True),
            ("Test", testPass, True)
        ]
    )
    
    fileMenu = menuBar.addMenu(
        "Intervals", commands = [
            ("Tutorial", testPass, True),
            ("Melodic", testPass, True),
            ("Harmonic", testPass, True)
        ]
    )
    
    fileMenu = menuBar.addMenu(
        "Chords", commands = [
            ("Tutorial", testPass, True),
            ("Chord Quality", testPass, True),
            ("Cadences", testPass, True),
        ]
    )
    
    fileMenu = menuBar.addMenu(
        "Terminology", commands = [
            ("Tutorial", testPass, True),
            ("Flash Cards", testPass, True)
        ]
    )
    
    fileMenu = menuBar.addMenu(
        "Instrument Practice", commands = [
        ("Choose Song", testPass, True)
        ]
    )
    
    fileMenu = menuBar.addMenu(
        "Preferences", commands = [
        ("Settings", testPass, True)
        ]
    )

    app.mainloop()
