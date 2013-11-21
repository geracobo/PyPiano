from kivy.core.audio import SoundLoader


class PianoKeys():
    def __init__(self):
        self.C4 = SoundLoader.load('keys/C4.ogg')
        self.D4 = SoundLoader.load('keys/D4.ogg')
        self.E4 = SoundLoader.load('keys/E4.ogg')
        self.F4 = SoundLoader.load('keys/F4.ogg')
        self.G4 = SoundLoader.load('keys/G4.ogg')
        self.A4 = SoundLoader.load('keys/A4.ogg')
        self.B4 = SoundLoader.load('keys/B4.ogg')
        self.C5 = SoundLoader.load('keys/C5.ogg')
        self.D5 = SoundLoader.load('keys/D5.ogg')
        self.E5 = SoundLoader.load('keys/E5.ogg')
        self.F5 = SoundLoader.load('keys/F5.ogg')
        self.G5 = SoundLoader.load('keys/G5.ogg')
        self.A5 = SoundLoader.load('keys/A5.ogg')
        self.B5 = SoundLoader.load('keys/B5.ogg')


