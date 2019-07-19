import tkinter as tk
from Globals import config


class SliderContainer(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent)

        self.model = model
        self.model.setView(self)

        self.slider = tk.Scale(
            self,
            from_=model.start,
            to=model.end,
            resolution=model.step,
            command=self.updateValue,
            orient=tk.HORIZONTAL
        )
        self.title = tk.Label(
            self,
            height=1,
            text=model.getTitle(),
            font=config.SMALL_FONT
        )
        self.title.pack(side=tk.LEFT, expand=1)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def updateValue(self, event):
        self.model.setValue(self.slider.get())

    def refresh(self):
        self.slider.set(self.model.getValue())
