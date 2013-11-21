from kivy.core.audio.audio_pygame import SoundPygame

from pygame import mixer
from pygame import sndarray
import math
import numpy

bits = 16

mixer.pre_init(44100, -bits, 2, 1024)
mixer.init()
mixer.set_num_channels(32)


class SoundPiano(SoundPygame):

    duration = 1.0
    freq = 440
    sample_rate = 44100
    n_samples = int(round(duration*sample_rate))

    def __init__(self):
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
        
        self._data = sndarray.make_sound(buf)
        super(SoundPiano, self).play()