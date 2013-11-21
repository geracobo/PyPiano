#!/usr/bin/env python

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock


import serial

import time

import thread
from Queue import Queue


from piano import PianoKeys

keys = PianoKeys()


def serial_thread(queue):
    ser = serial.Serial('/dev/ttyACM0', 9600)

    while(True):
        data = queue.get()
        data = str(data)

        print "Writing..."
        # for char in data:
        #     print char
        #     print ord(char)
        #     ser.write(char)
        ser.write(data)


        print "Reading..."
        ret = ser.readline()

        print ret
        queue.put(ret)
        time.sleep(1)

class RootWidget(BoxLayout):
    def on_C4(self):
        keys.C4.play()
    def on_D4(self):
        keys.D4.play()
    def on_E4(self):
        keys.E4.play()
    def on_F4(self):
        keys.F4.play()
    def on_G4(self):
        keys.G4.play()
    def on_A4(self):
        keys.A4.play()
    def on_B4(self):
        keys.B4.play()

class PianoApp(App):
    def build(self):
        return RootWidget()
