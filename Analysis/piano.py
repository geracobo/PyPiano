#!/usr/bin/env python
# coding=utf-8

import numpy as np
import wave
import matplotlib.pyplot as plt

class SoundFile:
   def  __init__(self, signal):
       self.file = wave.open('test.wav', 'wb')
       self.signal = signal
       self.sr = 44100

   def write(self):
       self.file.setparams((1, 2, self.sr, 44100*2, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()


def dec_to_amp(dec):
    return 10**(dec/20)


# Signal
duration = 2 # seconds
samplerate = float(44100) # Hz
samples = duration*samplerate
period = 1/samplerate

# Time axis
xaxis = np.arange(0, 2, period)*2*np.pi
#print xaxis


signal = np.zeros(len(xaxis))

import csv
reader = csv.reader(open('./spectrum.txt'), delimiter='\t')
for line in reader:
    hz = float(line[0])
    db = float(line[1])
    amp = dec_to_amp(db)
    #print hz,db,amp

    signal = np.add(signal, amp*np.sin(hz*xaxis))



#signal = np.sin(440*xaxis)
#print signal


# # Dominant signal
# signal = 0.38459178204535355*np.sin(440*xaxis)

# # Harmonics
# signal = np.add(signal, 0.03507518739525679*np.sin(507*xaxis))
# signal = np.add(signal, 0.01*np.sin(536*xaxis))
# signal = np.add(signal, 0.015848931924611134*np.sin(580*xaxis))
# signal = np.add(signal, 0.1333521432163324*np.sin(880*xaxis))
# signal = np.add(signal, 0.23713737056616552*np.sin(1323*xaxis))
# signal = np.add(signal, 0.020892961308540386*np.sin(1768*xaxis))




# # Subharmonics
# signal = np.add(signal, 0.043151907682776526*np.sin(372*xaxis))
# signal = np.add(signal, 0.008413951416451947*np.sin(318*xaxis))
# signal = np.add(signal, 0.017378008287493744*np.sin(240*xaxis))
# signal = np.add(signal, 0.03126079367123954*np.sin(147*xaxis))
# signal = np.add(signal, 0.030902954325135904*np.sin(110*xaxis))
# signal = np.add(signal, 0.034673685045253165*np.sin(75*xaxis))
# signal = np.add(signal, 0.10715193052376065*np.sin(31*xaxis))




# Gain
signal = 10000*signal

# Plot
#plt.plot(xaxis, signal)
#plt.show()



ssignal = ''
for i in range(len(signal)):
   ssignal += wave.struct.pack('h',signal[i]) # transform to binary

f = SoundFile(ssignal)
f.write()
print 'file written'