#!/usr/bin/env python
# coding=utf-8

from matplotlib import pyplot
import numpy as np
import csv

samplerate = 44100
period = 1/float(samplerate)

f = open('sample-data.csv')

y = np.empty((1))
time = np.empty((1))

at = float(0)
for row in f:
	data = row
	y=np.append(y,float(data))
	time=np.append(time, at)
	at = at+period


pyplot.plot(time, y)

def cn(n):
   c = y*np.exp(-1j*2*n*np.pi*time/period)
   return c.sum()/c.size
def f(x, Nh):
   f = np.array([2*cn(i)*np.exp(1j*2*i*np.pi*x/period) for i in range(1,Nh+1)])
   return f.sum()
y2 = np.array([f(t,50).real for t in time])

#pyplot.xlim(0,600)
pyplot.plot(time, y2)

pyplot.show()

print y