# Imports
from tkinter import *
from tkinter import messagebox
from ttkthemes import ThemedStyle
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Stops pygame welcome message
from pygame import mixer # https://stackoverflow.com/questions/17292444/pygame-mixer-save-audio-to-disk
from PIL import ImageTk, Image
from command import run # Used to run the console commands in Python, so IPython is not required # Example: res = command.run(['ls']) 

# Definitions
def testPopUp():
    messagebox.showinfo('Test', 'Testy test')

def clearPacks():
    # page.pack_forget()
    pass

# Pygame mixer
mixer.init()
mixer.set_num_channels(5)

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

# Setting up Tkinter window
window = Tk()
style = ThemedStyle(window)
style.set_theme("yaru") #Light mode is yaru, dark mode is equilux
window.configure(bg="floral white")
window.title("Basic outline")
window.geometry("1250x750")

# Creating the menu bar
menuBar = Menu(window)  

instrumentRoles = Menu(menuBar)
instrumentRoles.add_command(label="Rock Band")
menuBar.add_cascade(label="Instrument Roles", menu=instrumentRoles)

sightReading = Menu(menuBar)
sightReading.add_command(label="Tutorial")
sightReading.add_command(label="Test")
menuBar.add_cascade(label="Sight Reading", menu=sightReading)

interval = Menu(menuBar)
interval.add_command(label="Tutorial")
interval.add_command(label="Melodic")
interval.add_command(label="Harmonic")
menuBar.add_cascade(label="Interval", menu=interval)

chords = Menu(menuBar)
chords.add_command(label="Tutorial")
chords.add_command(label="Chord Quality")
chords.add_command(label="Cadences")
menuBar.add_cascade(label="Chords", menu=chords)

terminology = Menu(menuBar)
terminology.add_command(label="Tutorial")
terminology.add_command(label="Flash Cards")
menuBar.add_cascade(label="Terminology", menu=terminology)

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

# Testing adding a slider
def vocalVolume(x):
    volume = vocalsSlider.get()/100 # Range must be viewed as decimals between 0 - 1, so dividing by 100 makes it work
    channel5.set_volume(volume)

def drumsVolume(x):
    volume = drumsSlider.get()/100
    channel2.set_volume(volume)

vocalsSlider = Scale(window, from_ = 100, to = 0, command=vocalVolume)
vocalsSlider.set(100)
vocalsSlider.pack(side = LEFT)

drumsSlider = Scale(window, from_ = 100, to = 0, command = drumsVolume)
drumsSlider.set(100)
drumsSlider.pack(side = LEFT)

# Test adding an image
image1 = Image.open("images/test.png")
img = ImageTk.PhotoImage(image1)
panel = Label(window, image = img)
panel.pack()

# Keep the window running unless closed
if __name__ == "__main__":
    window.mainloop()
