##### Imports #####
# GUI creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle

# Music
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Stops pygame welcome message from showing
from pygame import mixer # To play the individual stems at the same time
try:
    from musicalbeeps import Player # To play to notes in test # https://pypi.org/projexct/musicalbeeps/

except ModuleNotFoundError: # This helps users have a better understanding on how to get the package to work
    from termcolor import colored
    
    link = colored("https://visualstudio.microsoft.com/visual-cpp-build-tools/", "blue")
    print('This program requires the module musicalbeeps. This package does require Microsoft Visual C++ 14.0 or greater. \nDownload "Microsoft C++ Build Tools" from ' + link + ' to get it.Select "Desktop development with C++" to ensure you install everything needed. \nDo this before doing pip install musicalbeeps.')
    exit()

##### Definitions #####
# Creating the menu bar
def clearFrame():
    # Destroy all the widgets
    '''
    for widget in frame.winfo_children():
        widget.destroy()
    '''

    # Clear frames
    '''
    frame.pack_forget()
    '''

def createMenuBar():
    menuBar = Menu(root)  

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

    root.config(menu=menuBar)

def testLabels():
    tktext = Label(root, text=" tk Label")
    tktext.pack()
    tkbutton = Button(root, text="tk Button")
    tkbutton.pack()

    text = ttk.Label(root, text=" ttk Label")
    text.pack()
    button = ttk.Button(root, text="ttk Button")
    button.pack()

# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

##### Main Loop #####
if __name__ == "__main__":    
    # Setup Tkinter window
    root = Tk()
    root.title('App')
    style = ThemedStyle(root)
    style.set_theme("yaru") # yaru is used for light mode, equilux is used for dark mode
    root.state('zoomed') # Makes the program take up fullscreen while being windowed

    createMenuBar()
    testLabels()

    root.lift() # To make sure the program opens in the foreground
    root.mainloop()
