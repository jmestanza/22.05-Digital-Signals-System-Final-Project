import tkinter as tk
import tkinter.ttk as ttk
from GuiUtils.PlotContainer import PlotContainer


class PlotContainerTabs(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)

        self.tabControl = ttk.Notebook(self)

        self.tab1 = PlotContainer(self.tabControl, "Tiempo (s)", "Amplitud (V)")
        self.tab2 = PlotContainer(self.tabControl, "Frecuencia (hz)", "Amplitud (V)")

        self.tabControl.add(self.tab1, text="Tiempo")
        self.tabControl.add(self.tab2, text="Frecuencia")

        self.tabControl.pack(side=tk.TOP, fill=tk.BOTH)

    def autoscale(self):
        self.tab1.autoscale()
        self.tab2.autoscale()