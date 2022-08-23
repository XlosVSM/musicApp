##### Imports #####
# GUI Creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle

# Misc
from darkdetect import isDark # Used for first time use

# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

##### Classes #####
class musicApp(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Music App")
        style = ThemedStyle(self)
        self.state("zoomed")
        style.set_theme(theme)
        
        container = ttk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        # Initialising frames to an empty array
        self.frames = {}
        
        # iterating through a tuple consisting of the different page layouts
        for i in (StartPage):
            frame = i(container, self)
            
            # initialising frame of that object from StartPage respectively with for loop
            self.frames[i] = frame
            
            frame.grid(row = 0, column = 0, sticky = "nsew")
            
        self.show_frame(StartPage)
        
class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        label = ttk.Label(self, text = "Test")
        
##### Definitions ######   
def settings():
    pass  
   
def createMenuBar():
    menuBar = Menu(app)  

    instrumentRoles = Menu(menuBar, tearoff="off") # tearoff removes dotted lines
    instrumentRoles.add_command(label="Rock Band")
    menuBar.add_cascade(label="Instrument Roles", menu=instrumentRoles)

    sightReading = Menu(menuBar, tearoff="off")
    sightReading.add_command(label="Tutorial")
    sightReading.add_command(label="Test")
    menuBar.add_cascade(label="Sight Reading", menu=sightReading)

    interval = Menu(menuBar, tearoff="off")
    interval.add_command(label="Tutorial")
    interval.add_command(label="Melodic")
    interval.add_command(label="Harmonic")
    menuBar.add_cascade(label="Interval", menu=interval)

    chords = Menu(menuBar, tearoff="off")
    chords.add_command(label="Tutorial")
    chords.add_command(label="Chord Quality")
    chords.add_command(label="Cadences")
    menuBar.add_cascade(label="Chords", menu=chords)

    terminology = Menu(menuBar, tearoff="off")
    terminology.add_command(label="Tutorial")
    terminology.add_command(label="Flash Cards")
    menuBar.add_cascade(label="Terminology", menu=terminology)

    instrumentPractice = Menu(menuBar, tearoff="off")
    instrumentPractice.add_command(label="Choose song")
    menuBar.add_cascade(label="Instrument Practice", menu = instrumentPractice)
    
    preferences = Menu(menuBar, tearoff="off")
    preferences.add_command(label="Settings", command = settings)
    menuBar.add_cascade(label = "Preferences", menu = preferences)

    app.config(menu=menuBar)
    
##### Main code #####    
if __name__ == "__main__":
    # Try getting the user's preferred theme
    try:
        with open('theme.txt') as f:
            theme = f.readline()
    
    # First time use
    except FileNotFoundError:
        darkMode = isDark()
        
        if darkMode == True:
            theme = "equilux"
        
        else:
            theme = "yaru"
        
        with open('theme.txt', 'w') as f:
            f.write(theme)
    
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
