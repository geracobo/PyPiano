from kivy.core.audio import SoundLoader


class PianoSounds():
    sounds = dict()
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

        self.sounds['C4'] = self.C4
        self.sounds['D4'] = self.D4
        self.sounds['E4'] = self.E4
        self.sounds['F4'] = self.F4
        self.sounds['G4'] = self.G4
        self.sounds['A4'] = self.A4
        self.sounds['B4'] = self.B4
        self.sounds['C5'] = self.C5
        self.sounds['D5'] = self.D5
        self.sounds['E5'] = self.E5
        self.sounds['F5'] = self.F5
        self.sounds['G5'] = self.G5
        self.sounds['A5'] = self.A5
        self.sounds['B5'] = self.B5
    def __getitem__(self, item):
        return self.sounds[item]

