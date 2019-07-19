from GuiUtils.InfoCard import InfoCard


class InfoModel:
    def __init__(self, text):
        self.text = text
        self.okText = False
        self.error = False

        self.view = None

    def getViewClass(self):
        return InfoCard

    def setView(self, view):
        self.view = view

    def setOk(self):
        self.ok = True
        if self.view:
            self.view.refresh()

    def setError(self):
        self.error = True
        if self.view:
            self.view.refresh()

    def getText(self):
        return self.text

    def getOk(self):
        return self.ok

    def getError(self):
        return self.error


