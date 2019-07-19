from GuiUtils.ChannelCard import ChannelCard


class ChannelModel:
    def __init__(self, id, name):
        self.viewClass = ChannelCard
        self.id = id
        self.name = name
        self.instrumento = None
        self.volume = 100
        self.enabled = True
        self.channelBackground = "blue"
        self.instrumentBackground = "pink"
        self.onConfigure = None
        self.view = None

    def getViewClass(self):
        return self.viewClass

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def setName(self, name):
        self.name = name
        return self

    def setView(self, view):
        self.view = view
        return self

    def setInstrumento(self, instrumento):
        self.instrumento = instrumento
        if self.view:
            self.view.refresh()
        return self

    def setVolume(self, volume):
        if self.view:
            self.view.refresh()
        self.volume = volume
        return self

    def setChannelBackground(self, color):
        self.channelBackground = color
        return self

    def setInstrumentBackground(self, color):
        self.instrumentBackground = color
        return self

    def setOnConfigureListener(self, action):
        self.onConfigure = action
        return self

    def getName(self):
        return self.name

    def getInstrumento(self):
        return self.instrumento

    def getVolume(self):
        return self.volume

    def getChannelBackground(self):
        return self.channelBackground

    def getInstrumentBacgrkound(self):
        return self.instrumentBackground

    def toggleEnable(self):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True

    def getEnabled(self):
        return self.enabled

    def getOnConfigureListener(self):
        return self.onConfigure

    def getInstrumentoName(self):
        if self.instrumento:
            return self.instrumento.getInstrumentData().getName()
        else:
            return "No hay instrumento seleccionado"
