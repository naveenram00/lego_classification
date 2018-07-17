try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *
try:
    import TkMessageBox
except ImportError:
    import tkinter.messagebox
import sys
import pygame

def destroy(self):
    self._error_window.destroy()
    
top = tkinter.Tk()
def complete():
    result = tkinter.messagebox.askquestion("Done", "Are You Sure?", icon='warning', bg="#b19cd9")
    if result == 'yes':
        print ("Confirmed")
        top.destroy()
    else:
        print ("Keep Selecting")
B1 = tkinter.Button(top, text = "Done", command = complete)
B1.pack()
top.mainloop()