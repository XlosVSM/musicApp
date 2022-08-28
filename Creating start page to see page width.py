from tkinter import *
from tkinter import ttk
from ttkthemes import *

root = Tk()
root.title("Test")

text = ttk.Label(root, text = "Music Learning App", font = ("Helvetica", 64))
print(text.winfo_width())
text.pack()
print(text.winfo_width())

root.mainloop()