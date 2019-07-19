

class SliderModel:
    def __init__(self, start, end, step, startValue, title, callOnChange = None):
        self.value = startValue
        self.start = start
        self.end = end
        self.step = step
        self.title = title
        self.view = None
        self.callOnChange = callOnChange

    def setView(self, view):
        self.view = view

    def getView(self):
        return self.view

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
        if self.view:
            self.view.refresh()
        if self.callOnChange:
            self.callOnChange(self.value)

    def getTitle(self):
        return self.title
