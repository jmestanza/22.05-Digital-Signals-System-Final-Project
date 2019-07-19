

class PlotSignals:
    plotSignals = None

    def __init__(self):
        self.signals = {}

    def setSignal(self, name, content):
        self.signals[name] = content


def getSignalsData():
    if not PlotSignals.plotSignals:
        PlotSignals.plotSignals = PlotSignals()
    return PlotSignals.plotSignals

