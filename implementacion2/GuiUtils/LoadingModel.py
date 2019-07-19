
class LoadingModel:
    def __init__(self, value, maxValue):
        self.value = value
        self.maxValue = maxValue
        self.container = None
        self.onLoaded = None

    def setOnLoadedListener(self, func):
        self.onLoaded = func

    def setContainer(self, container):
        self.container = container

    def update(self, value):
        self.value += value
        if self.container:
            self.container.refresh()

    def setValue(self, value):
        self.value = value
        if self.container:
            self.container.refresh()

    def reset(self):
        self.value = 0
        if self.container:
            self.container.refresh()

    def callOnFinished(self):
        if self.onLoaded:
            self.onLoaded()

    def getValue(self):
        return self.value

    def getMaxValue(self):
        return self.maxValue