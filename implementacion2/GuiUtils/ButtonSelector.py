import tkinter as tk
from tkinter import *
from Globals import config


class ButtonSelector(tk.Frame):
    def __init__(self, parent, buttonSelectorModel):
        tk.Frame.__init__(self, parent)

        self.var = StringVar()
        self.var.set("None")

        self.buttons = {}
        self.buttonSelectorModel = buttonSelectorModel
        self.buttonSelectorModel.setUpdateButtonsListener(self.generateButtons)

    def generateButtons(self):
        buttons = self.buttonSelectorModel.buttons

        for button in self.buttons.keys():
            self.buttons[button].pack_forget()

        i = 0

        self.buttons = {}

        for button in buttons.keys():
            self.buttons[button] = Radiobutton(self,
                                               text=buttons[button].title,
                                               indicatoron=0,
                                               width=20,
                                               value=button,
                                               variable=self.var,
                                               font=config.SMALLEST_FONT,
                                               command=buttons[button].callAction,
                                               background="cyan2",
                                               selectcolor="cyan4")

            self.buttons[button].pack(side=LEFT, fill=tk.X, expand=1)
            i = i + 1


