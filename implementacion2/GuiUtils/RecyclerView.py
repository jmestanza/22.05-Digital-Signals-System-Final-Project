import tkinter as tk
from GuiUtils.ChannelModel import ChannelModel
from GuiUtils.ChannelCard import ChannelCard


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


class RecyclerView(tk.Frame):
    def __init__(self, parent, controller, height=400):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.elements = []
        self.views = dict()

        self.container = tk.Canvas(
            self,
            width=600, height=height,
            borderwidth=5,
            background="#fff6fe"
        )

        self.vsb = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.container.yview
        )

        self.container.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.vsb.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.separation = 110
        self.start = 20

    def configureSeparation(self, separation):
        self.separation = separation

    def setStart(self, start):
        self.start = start

    def addElement(self, element):
        viewType = element.getViewClass()
        view = viewType(self.container, element)
        window = self.container.create_window(
            (300, self.start + self.separation * len(self.elements)),
            window=view
        )
        self.container.addtag_all("all")

        view.bind(
            "<Configure>",
            lambda event,
            canvas=self.container: onFrameConfigure(self.container)
        )

        self.views[element] = {"view": view, "window": window}
        self.elements.append(element)

    def clear(self):
        for element in self.elements:
            self.container.delete(self.views[element]["window"])

        self.elements = []

    def getElements(self):
        return self.elements

