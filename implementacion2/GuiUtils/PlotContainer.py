import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
import matplotlib.pyplot as plt
from tkinter import *


class PlotContainer(tk.Frame):
    def __init__(self, tabControl, xAxis, yAxis):
        super(PlotContainer, self).__init__(tabControl)
        self.graph = Canvas(self)

        self.fig, self.axis = plt.subplots()
        self.dataPlot = FigureCanvasTkAgg(self.fig, master=self.graph)
        #self.dataPlot.draw(self)

        self.nav = NavigationToolbar2Tk(self.dataPlot, self.graph)

        #self.dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.dataPlot._tkcanvas.pack(side=BOTTOM, fill=X, expand=1)

        self.graph.pack(side=TOP, expand=1, fill=BOTH)

        self.xAxis = xAxis
        self.yAxis = yAxis

    def plot(self, signal):
        x_lim_left, x_lim_right = self.axis.get_xlim()
        y_lim_left, y_lim_right = self.axis.get_ylim()

        self.axis.clear()

        #print(x_lim_left)
        if x_lim_left == 0.0:
            self.axis.autoscale()
        else:
            self.axis.set_xlim(x_lim_left, x_lim_right)
            self.axis.set_ylim(y_lim_left, y_lim_right)

        self.axis.set_xlabel(self.xAxis)
        self.axis.set_ylabel(self.yAxis)

        self.axis.plot(signal.xvar, signal.values)
        self.axis.minorticks_on()
        self.axis.grid(which='major', linestyle='-', linewidth=0.3, color='black')
        self.axis.grid(which='minor', linestyle=':', linewidth=0.1, color='black')

        self.dataPlot.draw()

    def autoscale(self):
        self.axis.autoscale()
