
class ButtonModel:
    def __init__(self, title, action):
        self.title = title
        self.action = action

    def setAction(self, action):
        self.action = action

    def callAction(self):
        if self.action:
            self.action()

