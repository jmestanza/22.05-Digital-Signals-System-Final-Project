import tkinter as tk
from Globals import config


class InfoCard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.controller.setView(self)

        self.contentText = tk.Label(
            self,
            height=1,
            text=self.controller.getText(),
            font=config.SMALL_FONT,
            background="#fffa95"
        )
        self.contentText.grid(column=0, row=0)

        self.infoText = tk.Label(
            self,
            height=1,
            text="...",
            font=config.SMALL_FONT,
            background="#fffa95"
        )

        self.infoText.grid(column=1, row=0)

    def refresh(self):
        pass
