import tkinter as ttk
from tkinter.ttk import Progressbar


class LoadingContainer(ttk.Frame):
    def __init__(self, parent, model):
        super(LoadingContainer, self).__init__(parent)
        self.model = model

        self.progressBar = Progressbar(
            self, orient=ttk.HORIZONTAL,
            length=self.model.getMaxValue(), mode='determinate',
            style="red.Horizontal.TProgressbar"
        )
        self.progressBar.pack(side=ttk.TOP, fill=ttk.X, expand=1)

    def refresh(self):
        self.progressBar["value"] = self.model.getValue()

    def destroy(self):
        print("destroy")
        self.progressBar.destroy()
