import tkinter as tk
from Globals import config
from threading import Thread
from util_python.soundUtils import playSound, reescale

class ChannelCard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.setView(self)

        self.upFrame = UpFrame(self, controller)
        self.upFrame.pack(side=tk.TOP, fill=tk.BOTH)

        self.content = ContentFrame(self, controller)
        self.content.pack(side=tk.TOP, fill=tk.BOTH)

    def toggleDisable(self):
        self.controller.toggleEnable()
        if self.controller.getEnabled():
            self.upFrame.enable()
            self.content.enable()
        else:
            self.upFrame.disable()
            self.content.disable()

    def refresh(self):
        self.content.title.configure(
            text=self.controller.getInstrumentoName()
        )
        self.upFrame.textVol.configure(
            text="VOL: "+str(self.controller.getVolume())
        )


class UpFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="sandy brown")
        self.parent = parent

        self.controller = controller

        self.title = tk.Label(
            self,
            height=1,
            text=self.controller.getName(),
            font=config.SMALL_FONT,
            background="sandy brown"
        )
        self.title.grid(column=0, row=0)

        self.textVol = tk.Label(
            self,
            height=1,
            text="VOL: "+str(self.controller.getVolume()),
            font=config.LARGE_FONT,
            background="sandy brown"
        )

        self.textVol.grid(column=1, row=0)

        self.buttonDisable = tk.Button(
            self,
            height=1,
            width=10,
            text="Desactivar",
            background="tomato",
            font=config.SMALLEST_FONT,
            command=self.parent.toggleDisable,
        )
        self.buttonDisable.grid(column=2, row=0)

        self.grid_columnconfigure(0, weight=15)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def enable(self):
        self.configure(bg="sandy brown")
        self.title.configure(bg="sandy brown")
        self.textVol.configure(bg="sandy brown")
        self.buttonDisable.configure(bg="tomato", text="Desactivar")

    def disable(self):
        self.configure(bg="gray")
        self.title.configure(bg="gray")
        self.textVol.configure(bg="gray")
        self.buttonDisable.configure(bg="chartreuse3", text="Activar")


class ContentFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="thistle1")

        self.controller = controller

        self.title = tk.Label(
            self,
            height=2,
            width=30,
            text=self.controller.getInstrumentoName(),
            font=config.SMALL_FONT,
            background="#c9a3ff"
        )
        self.title.grid(column=0, row=0)

        self.frameButtons = tk.Frame(self)

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)

        self.buttonPlay = tk.Button(
            self.frameButtons,
            height=1,
            width=20,
            text="Escuchar",
            background="light goldenrod",
            font=config.SMALLEST_FONT,
            command=self.play
        )

        self.buttonConfig = tk.Button(
            self.frameButtons,
            height=1,
            width=20,
            text="Configurar",
            background="SteelBlue1",
            font=config.SMALLEST_FONT,
            command=self.controller.getOnConfigureListener().onAction
        )

        self.buttonPlay.grid(column=0, row=0)
        self.buttonConfig.grid(column=0, row=1)

        self.frameButtons.grid(column=1, row=0)
        self.playing = False

    def enable(self):
        self.configure(bg="sandy brown")
        self.title.configure(bg="#c9a3ff", text=self.controller.getInstrumento())
        self.buttonPlay.configure(state=tk.NORMAL, bg="light goldenrod")
        self.buttonConfig.configure(state=tk.NORMAL, bg="SteelBlue1")

    def disable(self):
        self.configure(bg="snow4")
        self.title.configure(bg="snow4", text="Desactivado")

        self.buttonPlay.configure(state=tk.DISABLED, bg="snow4")
        self.buttonConfig.configure(state=tk.DISABLED, bg="snow4")

    def play(self):
        if not self.playing:
            if self.controller.getInstrumento():
                if len(self.controller.getInstrumento().getInstrumentData().getSound()) > 0:
                    self.playing = True
                    sound = self.controller.getInstrumento().getInstrumentData().getSound().copy()
                    reescale(sound, self.controller.getVolume())
                    self.thread = Thread(
                        target=playSound,
                        args=(sound, config.fs, self.controller.getVolume(), lambda: self.callWhenEnd() )
                    )

                    self.thread.start()

    def callWhenEnd(self):
        self.playing = False
