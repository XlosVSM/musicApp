'''
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

root = tk.Tk()
root.title('App')

style = ThemedStyle(root)
style.set_theme("yaru")

height = root.winfo_height()
width = root.winfo_width()
    
homeFrame = ttk.Frame(root, height = height, width = width)
homeFrame.pack()

tktext = tk.Label(root, text=" tk Label")
tktext.pack()
tkbutton = tk.Button(root, text="tk Button")
tkbutton.pack()

text = ttk.Label(root, text=" ttk Label")
text.pack()
button = ttk.Button(root, text="ttk Button")
button.pack()

root.geometry('200x200')

root.mainloop()
'''
# Imports
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle

def createFrames():
    global homeFrame

    height = root.winfo_height()
    width = root.winfo_width()

    homeFrame = ttk.Frame(root, height = height, width = width)

def homePage():
    homeFrame.pack()

##### Main Loop #####
# Setup Tkinter window
root = Tk()
root.title('App')
style = ThemedStyle(root)
root.state('zoomed')

style.set_theme("yaru")

createFrames()
homePage()

root.lift()
root.mainloop()
