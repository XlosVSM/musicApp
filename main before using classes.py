##### Imports #####
# GUI creation
from tkinter import *
from tkinter import ttk # So I can use themed widgets
from ttkthemes import ThemedStyle

# Music
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Stops pygame welcome message from showing
from pygame import mixer # To play the individual stems simultaneously
'''
try:
    from musicalbeeps import Player # To play to notes in test # https://pypi.org/projexct/musicalbeeps/

except ModuleNotFoundError: # This helps users have a better understanding on how to get the package to work
    from termcolor import colored
    
    link = colored("https://visualstudio.microsoft.com/visual-cpp-build-tools/", "blue")
    print('This program requires the module musicalbeeps. This package does require Microsoft Visual C++ 14.0 or greater. \nDownload "Microsoft C++ Build Tools" from ' + link + ' to get it.Select "Desktop development with C++" to ensure you install everything needed. Do this before doing pip install musicalbeeps. If you are using a Mac, you will not need to install this.')
    exit()
'''
# Miscellaneous
from darkdetect import isDark # Used for start up mode

##### Definitions #####
# Creating the menu bar
def clearFrames():
    # Destroy all the widgets
    for widget in homeFrame.winfo_children():
        widget.destroy()
    
    for widget in instrumentRolesFrame.winfo_children():
        widget.destroy()
        
    for widget in tutorialFrame.winfo_children():
        widget.destroy()
        
    for widget in testFrame.winfo_children():
        widget.destroy()
        
    for widget in flashCardsFrame.winfo_children():
        widget.destroy()
        
    for widget in songChoiceFrame.winfo_children():
        widget.destroy()
        
    for widget in musicPlayerFrame.winfo_children():
        widget.destroy()
        
    for widget in settingsFrame.winfo_children():
        widget.destroy()

    # Clear frames
    homeFrame.pack_forget()
    instrumentRolesFrame.pack_forget()
    tutorialFrame.pack_forget()
    testFrame.pack_forget()
    flashCardsFrame.pack_forget()
    songChoiceFrame.pack_forget()
    musicPlayerFrame.pack_forget()
    settingsFrame.pack_forget()

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
    
    preferences = Menu(menuBar, tearoff="off")
    preferences.add_command(label="Settings", command = settings)
    menuBar.add_cascade(label = "Preferences", menu = preferences)

    root.config(menu=menuBar)

# Page commands
def home():
    global testButton 
    
    clearFrames()
    homeFrame.pack()
    testButton = ttk.Button(root, text = "Test")
    testButton.pack()

def settings():
    clearFrames()
    settingsFrame.pack()   
        
# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

##### Main Loop #####
if __name__ == "__main__":
    try:
        with open('theme.txt') as f:
            line = f.readline()
            
        if line == "dark":
            theme = "equilux"
        
        elif line == "light":
            theme = "yaru"
            
        else: # If file is tampered with
            print("Please delete the file theme.txt and run the code again.")
            exit()
    
    except FileNotFoundError:
        darkMode = isDark() # Gets the users OS mode to be starter
        
        if darkMode == True:
            theme = "equilux"
            
            with open('theme.txt', 'w') as f:
                f.write("dark")
        
        else:
            theme = "yaru"
            
            with open('theme.txt', 'w') as f:
                f.write("light")
    
    # Setup Tkinter window
    root = Tk()
    root.title("App")
    style = ThemedStyle(root)
    root.state('zoomed')
    style.set_theme(theme)
    
    # Create frames
    height = root.winfo_height()
    width = root.winfo_width()
    
    homeFrame = ttk.Frame(root, height = height, width = width)
    instrumentRolesFrame = ttk.Frame(root, height = height, width = width)
    tutorialFrame = ttk.Frame(root, height = height, width = width)
    testFrame = ttk.Frame(root, height = height, width = width)
    flashCardsFrame = ttk.Frame(root, height = height, width = width)
    songChoiceFrame = ttk.Frame(root, height = height, width = width)
    musicPlayerFrame = ttk.Frame(root, height = height, width = width)
    settingsFrame = ttk.Frame(root, height = height, width = width)
    
    createMenuBar()
    home()

    root.mainloop()
