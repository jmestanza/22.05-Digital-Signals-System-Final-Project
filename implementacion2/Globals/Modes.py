import tkinter as tk


class Modes:
    def __init__(self):
        self.modesEnabled = None
        self.filename = None

    def start(self):
        self.modesEnabled = {
            "FAA": tk.IntVar(),
            "Sample and Hold": tk.IntVar(),
            "Llave analógica": tk.IntVar(),
            "FR": tk.IntVar()
        }

    def setFilename(self, filename):
        self.filename = filename

    def getFilename(self):
        return self.filename


modes = Modes()


def getModes():
    if not modes.modesEnabled:
        modes.start()
    return modes
