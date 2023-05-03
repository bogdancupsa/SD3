import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from memento import Memento
from observable import Observable
from observer import Observer

class CUPSA_IDE(Observable):
    
    __root = Tk()
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # Scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None
    __undo_stack = []

    def __init__(self, **kwargs):
        super().__init__()

        # Icon
        try:
            self.__root.wm_iconbitmap("lewis.ico")
        except:
            pass

        # Window size
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass    

        # Window text
        self.__root.title("CUPSA IDE")

        # Center Window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # Left align
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # Right align
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # Top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        # Autoresizable text area
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # Open a new file
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)

        # Open already existing file
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)

        # Save current file
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)

        # Create line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # Cut
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)

        # Copy
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)

        # Paste
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)

        # Undo
        self.__thisEditMenu.add_command(label="Undo", command=self.__undo)

        # Edit
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # Description feature
        self.__thisHelpMenu.add_command(label="About CUPSA IDE", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)
        self.__root.config(menu=self.__thisMenuBar)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Adjustable Scrollbar
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("CUPSA IDE", "Cupsa Bogdan")

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            # Try to open the file and set the window title accordingly
            self.__root.title(os.path.basename(self.__file) + "")
            self.__thisTextArea.delete(1.0, END)
            file = open(self.__file, "r")
            self.__thisTextArea.insert(1.0, file.read())
            file.close()
            self.notify_observers("File opened", self.__file)

    def __newFile(self):
        self.__root.title("Untitled")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)
        self.notify_observers("New file")

    def __saveFile(self):
        if self.__file == None:
            # Save as a new file
            self.__file = asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if self.__file == "":
                self.__file = None
            else:
                # Try to change the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close

                # Change window title
                self.__root.title(os.path.basename(self.__file) + "")
                self.notify_observers("File saved", self.__file)

        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()
            self.notify_observers("File saved", self.__file)

    def __cut(self):
        self.__save_undo_state()
        self.__thisTextArea.event_generate("<<Cut>>")        

    def __copy(self):
        self.__save_undo_state()
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__save_undo_state()
        self.__thisTextArea.event_generate("<<Paste>>")
        
    def __undo(self):
        if self.__undo_stack:
            memento = self.__undo_stack.pop()
            self.__thisTextArea.delete(1.0, END)
            self.__thisTextArea.insert(1.0, memento.text)

    def __save_undo_state(self):
        text = self.__thisTextArea.get(1.0, END)
        memento = Memento(text)
        self.__undo_stack.append(memento)

    def run(self):
        self.__root.mainloop()

Observer1 = Observer()
Observer2 = Observer()
MyObservable = CUPSA_IDE()
MyObservable.add_observer(Observer1)
MyObservable.add_observer(Observer2)

cupsa_ide = CUPSA_IDE(width=600, height=400)
cupsa_ide.run()

