# Imports
from tkinter import *
from tkinter import messagebox
from ttkthemes import ThemedStyle
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Definitions
def testPopUp():
    messagebox.showinfo('Test', 'Testy test')

def clearPacks():
    # page.pack_forget()
    pass

# Setting up Tkinter window
window = Tk()
style = ThemedStyle(window)
style.set_theme("yaru") #Light mode is yaru, dark mode is equilux
window.configure(bg="floral white")
window.title("Basic outline")
window.geometry("1250x750")

# Creating the menu bar
menuBar = Menu(window)  
file = Menu(menuBar)  
file.add_command(label="New")  
file.add_command(label="Open")
file.add_command(label="Save")  
file.add_command(label="Save as")    
file.add_separator()  
file.add_command(label="Exit", command=window.quit)  
menuBar.add_cascade(label="File", menu=file)  

sightReading = Menu(menuBar)
sightReading.add_command(label="Tutorial")
sightReading.add_command(label="Test")
menuBar.add_cascade(label="Sight Reading", menu=sightReading)

interval = Menu(menuBar)
interval.add_command(label="Tutorial")
interval.add_command(label="Melodic")
interval.add_command(label="Harmonic")
menuBar.add_cascade(label="Interval", menu=interval)

dictation = Menu(menuBar)
dictation.add_command(label="Tutorial")
dictation.add_command(label="Melodic")
dictation.add_command(label="Rhythmic")
menuBar.add_cascade(label="Dictation", menu=dictation)

chords = Menu(menuBar)
chords.add_command(label="Tutorial")
chords.add_command(label="Progressions")
chords.add_command(label="Chord Quality")
chords.add_command(label="7th Chord Quality")
menuBar.add_cascade(label="Chords", menu=chords)

instrumentPractice = Menu(menuBar)
instrumentPractice.add_command(label="Choose song")
menuBar.add_cascade(label="Instrument Practice", menu = instrumentPractice)

window.config(menu=menuBar)

canvas= Canvas(window, width= 500, height= 50, bg="SpringGreen2")

#Add a text in Canvas
canvas.create_text(250, 20, text="HELLO WORLD", fill="black", font=('Helvetica 15 bold'))
canvas.pack()


# Testing adding a button
btn = Button(window, text = "Grade One", command = testPopUp, highlightbackground = "floral white")
btn.pack()

# Keep the window running unless closed
window.mainloop()
