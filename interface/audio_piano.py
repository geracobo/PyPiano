from kivy.core.audio.audio_pygame import SoundPygame

from pygame import mixer
from pygame import sndarray
import math
import numpy

import csv


bits = 16

mixer.pre_init(44100, -bits, 2, 1024)
mixer.init()
mixer.set_num_channels(32)


def dec_to_amp(dec):
    return 10**(dec/20)

class Spectra():
    def __init__(self, freq, amp):
        self.frequency = freq
        self.amplitude = amp
    def __repr__(self):
        return str.format("({0}, {1})", self.frequency, self.amplitude)

class SoundPiano(SoundPygame):

    duration = 1.0
    freq = 440
    sample_rate = 44100
    n_samples = int(round(duration*sample_rate))

    spectrum = list()

    def __init__(self):
        reader = csv.reader(open('./spectrum.txt'), delimiter='\t')
        for line in reader:
            hz = float(line[0])
            db = float(line[1])
            amp = dec_to_amp(db)
            spec = Spectra(hz, amp)
            self.spectrum.append(spec)


        super(SoundPiano, self).__init__()

    def play(self):
        #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
        buf = numpy.zeros((self.n_samples, 2), dtype = numpy.int16)
        max_sample = 2**(bits - 1) - 1

        for s in range(self.n_samples):
            t = float(s)/self.sample_rate

            # Left speaker
            buf[s][0] = int(round(max_sample*math.sin(2*math.pi*self.freq*t)))
            # Right speaker...
            buf[s][1] = int(round(max_sample*math.sin(2*math.pi*self.freq*t)))
        print self.spectrum
        self._data = sndarray.make_sound(buf)
        super(SoundPiano, self).play()

    def tune(self, tones):
        spectrum = list()
        for spectra in self.spectrum:
            spec = Spectra(spectra.frequency*(2.0**(tones/12.0)), spectra.amplitude)
            spectrum.append(spec)
        return spectrum

    def playKey(self, key):
        buf = numpy.zeros((self.n_samples, 2), dtype = numpy.int16)
        max_sample = 2**(bits - 1) - 1

        print self.spectrum
        spectrum = self.tune(key)
        print spectrum

        for s in range(self.n_samples):
            t = float(s)/self.sample_rate



            for spectra in spectrum:
                # Left speaker
                buf[s][0] = buf[s][0] + int(round(max_sample*spectra.amplitude*math.sin(2*math.pi*spectra.frequency*t)))
                # Right speaker...
                buf[s][1] = buf[s][1] + int(round(max_sample*spectra.amplitude*math.sin(2*math.pi*spectra.frequency*t)))
        self._data = sndarray.make_sound(buf)
        super(SoundPiano, self).play()