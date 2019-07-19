

class ButtonSelectorModel:
    def __init__(self):
        self.onButtonGenerated = None

        self.buttonSelected = None
        self.buttons = {}

    def setButtons(self, buttons):
        self.buttons = buttons
        if self.onUpdateButtons:
            self.onUpdateButtons()

    def setUpdateButtonsListener(self, onUpdateButtons):
        self.onUpdateButtons = onUpdateButtons

    def buttonSelected(self, buttonName):
        self.onButtonSelected = buttonName
        if self.onButtonSelected:
            self.onButtonSelected()

