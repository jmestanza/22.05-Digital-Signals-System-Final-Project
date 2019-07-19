

class Listener:
    def __init__(self, action, *args):
        self.action = action
        self.args = args

    def onAction(self):
        self.action(*self.args)

    def onActionWithCustomArgs(self, *args):
        self.action(*args)
