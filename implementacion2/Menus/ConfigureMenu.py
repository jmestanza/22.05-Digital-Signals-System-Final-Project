import tkinter as tk
from tkinter import filedialog
from Menus.PlotMenu import PlotMenu
from GuiUtils.SliderContainer import SliderContainer
from GuiUtils.SliderModel import SliderModel
from GuiUtils.LoadingContainer import LoadingContainer
from GuiUtils.LoadingModel import LoadingModel
from Globals import Modes
import ntpath
from Globals import config
from threading import Thread


class ConfigureMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, height=2, text="Configuración", font=config.LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH)

        self.filename = ""

        self.btnText = tk.StringVar()

        self.buttonSelectFile = tk.Button(
            self,
            height=2,
            width=44,
            textvariable=self.btnText,
            background="dodger blue",
            font=config.SMALL_FONT,
            command=self.searchFile
        )
        self.btnText.set("Seleccionar entrada")

        self.slider1 = SliderModel(1, 5000, 5, config.GetConfigData().FAAfreq, "Sample rate (hz)")
        self.slider1cont = SliderContainer(self, self.slider1)
        self.slider1cont.pack(side=tk.TOP, fill=tk.BOTH)

        self.slider1.setContainer(self.slider1cont)
        self.slider1.setValue(config.GetConfigData().fs)

        self.slider2 = SliderModel(2, 98, 1, config.GetConfigData().FAAfreq, "Sample cycle (%)")
        self.slider2cont = SliderContainer(self, self.slider2)
        #print(config.GetConfigData().SHhold)

        self.slider2.setContainer(self.slider2cont)
        self.slider2.setValue(config.GetConfigData().SHhold*100)

        self.slider2cont.pack(side=tk.TOP, fill=tk.BOTH)

        self.buttonSelectFile.pack(side=tk.TOP, fill=tk.BOTH)

        for mode in Modes.getModes().modesEnabled.keys():
            checkButton = tk.Checkbutton(
                self,
                text=mode,
                variable=Modes.getModes().modesEnabled[mode],
                height=3,
                width=44,
                font=config.SMALL_FONT,
                background="light yellow"
            )

            checkButton.pack(side=tk.TOP, fill=tk.BOTH)
        self.loadingModel = None
        self.isLoading = False
        self.loadingModel = LoadingModel(0, 100)
        self.loading = LoadingContainer(self, self.loadingModel)
        self.loadingModel.setContainer(self.loading)
        self.loading.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.loadingModel.setOnLoadedListener(
            self.onDataCalc
        )

        self.button = tk.Button(
            self,
            height=1,
            width=44,
            background="pale green",
            text="ACEPTAR",
            font=config.LARGE_FONT,
            command=lambda: self.goToPlotMenu()
        )
        self.button.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def focus(self):
        self.loadingModel.reset()
        self.button.configure(state=tk.NORMAL)

    def searchFile(self):
        tk.Tk().withdraw()
        Modes.getModes().setFilename(filedialog.askopenfilename())

        self.btnText.set("Seleccionar entrada [" + ntpath.basename(Modes.getModes().getFilename()) + "]")

    def goToPlotMenu(self):
        if Modes.getModes().getFilename() and not self.isLoading:
            config.GetConfigData().setFs(self.slider1.getValue())
            config.GetConfigData().setSampleCycle(self.slider2.getValue())

            config.GetConfigData().save()
            config.GetConfigData().load()

            self.button.configure(state=tk.DISABLED)

            self.isLoading = True

            thread = Thread(target=ProcessSignals.processSignals,
                            args=(Modes.getModes().getFilename(), Modes.getModes().modesEnabled, self.loadingModel))
            thread.start()

    def onDataCalc(self):
        self.controller.showFrame(PlotMenu)

        self.isLoading = False

