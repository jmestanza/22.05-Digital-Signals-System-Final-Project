

class SyntetizeConfig:
    def __init__(self, channels, midiFilename):
        self.midiFilename = midiFilename
        self.channels = channels

    def getMidiFilename(self):
        return self.midiFilename

    def getChannels(self):
        return self.channels