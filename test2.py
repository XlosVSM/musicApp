#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
from tkinter import font  as tkfont



class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Window")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Home_Page, Insert_Page, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        menubar = MenuBar(self)
        self.config(menu=menubar)


        w = 800 # width for the Tk root
        h = 650 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/4) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))



        self.show_frame("Home_Page")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        filemenu = Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=filemenu)
        filemenu.add_command(label="New", command = self.donothing)
        filemenu.add_command(label = "Open", command = self.donothing)
        filemenu.add_command(label = "Save", command = self.donothing)
        filemenu.add_command(label = "Save as...", command = self.donothing)
        filemenu.add_command(label = "Close", command = self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self.quit)

        editmenu = Menu(self, tearoff=False)
        self.add_cascade(label = "Edit", menu = editmenu)
        editmenu.add_command(label = "Undo", command = self.donothing)
        editmenu.add_separator()
        editmenu.add_command(label = "Cut", command = self.donothing)
        editmenu.add_command(label = "Copy", command = self.donothing)
        editmenu.add_command(label = "Paste", command = self.donothing)
        editmenu.add_command(label = "Delete", command = self.donothing)
        editmenu.add_command(label = "Select All", command = self.donothing)

        recordsmenu = Menu(self, tearoff=False)
        self.add_cascade(label="Records", underline=0, menu=recordsmenu)
        recordsmenu.add_command(label="Insert", command=lambda: SampleApp().show_frame("Insert_Page"))
        recordsmenu.add_command(label="Search", command=lambda: SampleApp().show_frame("PageTwo"))

        helpmenu = Menu(self, tearoff=False)
        self.add_cascade(label = "Help", menu = helpmenu)
        helpmenu.add_command(label = "Help Index", command = self.donothing)
        helpmenu.add_command(label = "About...", command = self.donothing)

    def quit(self):
        sys.exit(0)

    def donothing(self):
        filewin = Toplevel()
        button = Button(filewin, text="Do nothing button")
        button.pack()


class Home_Page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Page One", command=lambda: controller.show_frame("Insert_Page"))
        button2 = Button(self, text="Page Two", command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class Insert_Page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        page = ttk.Notebook(self)
        tab1 = ttk.Frame(page)
        tab2 = ttk.Frame(page)
        tab3 = ttk.Frame(page)

        page.add(tab1, text='One')
        page.add(tab2, text='Two')
        page.add(tab3, text='three')

        page.pack(fill=BOTH, expand=1)

        day_label = Label(tab1, text="Tab1:")
        day_label.pack()
        day_label.place(x=0, y=30)
        day_label = Label(tab2, text="Tab2:")
        day_label.pack()
        day_label.place(x=0, y=30)
        day_label = Label(tab3, text="Tab3:")
        day_label.pack()
        day_label.place(x=0, y=30)

        button = Button(self, text="Go to the start page", command=lambda: controller.show_frame("Home_Page"))
        button.pack()


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page", command=lambda: controller.show_frame("Home_Page"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
    