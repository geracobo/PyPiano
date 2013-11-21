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

from audio import PianoSounds
keys = PianoSounds()


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

class PianoKey(Button):
    def __init__(self, key):
        super(PianoKey, self).__init__()

        self.key = key
        self.text = key
        self.color = [0,0,0,1]
        self.background_normal = "gui/img/key.jpg"
        self.background_down = "gui/img/key_down.jpg"

    def on_state(self, instance, value):
        if value == 'down':
            keys[self.key].play()


class PianoKeyboard(BoxLayout):
    def __init__(self):
        super(PianoKeyboard, self).__init__()

        self.orientation = 'horizontal'
        self.spacing = 1

        self.C4key = PianoKey('C4')
        self.D4key = PianoKey('D4')
        self.E4key = PianoKey('E4')
        self.F4key = PianoKey('F4')
        self.G4key = PianoKey('G4')
        self.A4key = PianoKey('A4')
        self.B4key = PianoKey('B4')
        self.C5key = PianoKey('C5')
        self.D5key = PianoKey('D5')
        self.E5key = PianoKey('E5')
        self.F5key = PianoKey('F5')
        self.G5key = PianoKey('G5')
        self.A5key = PianoKey('A5')
        self.B5key = PianoKey('B5')

        self.add_widget(self.C4key)
        self.add_widget(self.D4key)
        self.add_widget(self.E4key)
        self.add_widget(self.F4key)
        self.add_widget(self.G4key)
        self.add_widget(self.A4key)
        self.add_widget(self.B4key)
        self.add_widget(self.C5key)
        self.add_widget(self.D5key)
        self.add_widget(self.E5key)
        self.add_widget(self.F5key)
        self.add_widget(self.G5key)
        self.add_widget(self.A5key)
        self.add_widget(self.B5key)

class ModeSelector(Button):
    FREE_MODE = 0
    GAME_MODE = 1
    mode = FREE_MODE
    def __init__(self):
        super(ModeSelector, self).__init__()
        self.size_hint = (None, .5)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.width = 100
        self.text = "Modo Libre"

    def on_press(self):
        if self.mode == self.FREE_MODE:
            self.mode = self.GAME_MODE
            self.text = "Modo Juego"
            pass
        elif self.mode == self.GAME_MODE:
            self.mode = self.FREE_MODE
            self.text = "Modo Libre"
            pass
        else:
            #wtf
            pass


class MainMenu(BoxLayout):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.size_hint = (1, None)
        self.height = 60

        self.padding = [5, 0, 0, 0]

        self.add_widget(ModeSelector())

class LogBox(TextInput):
    def __init__(self):
        super(LogBox, self).__init__()
        #self.size_hint = (1, None)
        #self.height = 300

class RootWidget(BoxLayout):
    def __init__(self):
        super(RootWidget, self).__init__()
        self.orientation = "vertical"
        self.add_widget(MainMenu())
        self.add_widget(LogBox())
        self.add_widget(PianoKeyboard())

class PianoApp(App):
    def build(self):
        return RootWidget()
