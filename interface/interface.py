#!/usr/bin/env python

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import serial

import time

import thread
from Queue import Queue



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


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.textin = TextInput()
        self.textin.size_hint= (.5, .1)
        self.textin.pos_hint={'center_x':.5,
                            'center_y':.7}

        self.add_widget(self.textin)

        self.send = Button()
        self.send.text = 'Send'
        self.send.size_hint = (.3, .1)
        self.send.pos_hint = {'center_x': .5, 'center_y': .5}

        self.send.bind(on_press=self.on_send)

        self.add_widget(self.send)

        self.textout = TextInput()
        self.textout.size_hint= (.5, .1)
        self.textout.pos_hint={'center_x':.5,
                            'center_y':.3}

        self.add_widget(self.textout)

        self.queue = Queue()
        thread.start_new_thread(serial_thread, (self.queue,))


        Clock.schedule_interval(self.on_clock, .5)

    def on_send(self, instance):
        self.queue.put(self.textin.text)

        self.textin.text = ''
        self.textout.text = ''

        sound.play()

    def on_clock(self, dt):
        try:
            ret = self.queue.get(False)
            self.textout.text = ret
        except:
            pass




class PianoApp(App):

    def build(self):
        self.root = RootWidget()
        return self.root
