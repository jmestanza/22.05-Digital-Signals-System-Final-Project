import Globals.RWconfig as RWconfig

LARGE_FONT = ("Bahnschrift", 20)
SMALL_FONT = ("Bahnschrift", 16)
SMALLEST_FONT = ("Bahnschrift", 10)
debug = True
fs = 44100
imageFilename = None

# los valores no son los reales


class ConfigData:
    def __init__(self):
        self.FAAfreq = None
        self.SHsample = None
        self.SHhold = None
        self.fs = None

        self.LLfreq = None
        self.LLoff = None
        self.LLon = None
        self.Transitorio = None

        self.loaded = False

    def setLoaded(self):
        self.loaded = True

    def load(self):
        RWconfig.loadConfig(self)

    def save(self):
        RWconfig.writeConfig(self)

    def setFs(self, value):
        self.fs = value
        self.LLfreq = value

    def setSampleCycle(self, value):
        self.SHsample = value / 100
        self.SHhold = 1 - self.SHsample

        self.LLoff = self.SHsample
        self.LLon = self.SHhold


configData = ConfigData()


def GetConfigData():
    if not configData.loaded:
        configData.load()
        configData.loaded = True

    return configData

