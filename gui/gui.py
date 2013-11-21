#!/usr/bin/env python

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

from arduino import Arduino
arduino = Arduino()

from audio import PianoSounds
keys = PianoSounds()




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



class PlayPauseButton(Button):
    PAUSE_MODE = 0
    PLAY_MODE = 1
    mode = PAUSE_MODE
    def __init__(self):
        super(PlayPauseButton, self).__init__()
        self.text = "Reproducir"

    def on_press(self):
        if self.mode == self.PAUSE_MODE:
            self.mode = self.PLAY_MODE
            self.text = "Pausar"
            pass
        elif self.mode == self.PLAY_MODE:
            self.mode = self.PAUSE_MODE
            self.text = "Reproducir"
            pass

class ConnectionBox(BoxLayout):
    def __init__(self):
        super(ConnectionBox, self).__init__()

        self.size_hint = (None, 1)
        self.width = 400

        self.statusLabel = Label()
        self.statusLabel.text = "Desconectado"
        self.statusLabel.color = [1,0,0,1]

        self.statusButton = Button()
        self.statusButton.text = "Conectarse"
        self.statusButton.bind(on_press=self.status_pressed)

        self.add_widget(Label(text='Estatus:'))
        self.add_widget(self.statusLabel)
        self.add_widget(self.statusButton)

    def status_pressed(self, instance):
        if self.statusButton.text == "Conectarse":
            arduino.connect()
        else:
            arduino.disconnect()

    def on_connect(self):
        self.statusLabel.text = "Conectado"
        self.statusLabel.color = [0,1,0,1]
        self.statusButton.text = "Desconectarse"
    def on_disconnect(self):
        self.statusLabel.text = "Desconectado"
        self.statusLabel.color = [1,0,0,1]
        self.statusButton.text = "Conectarse"


class MainMenu(BoxLayout):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.size_hint = (1, None)
        self.height = 40

        self.spacing = 10
        self.padding = [5, 5, 5, 5]

        self.playPauseButton = PlayPauseButton()
        self.playPauseButton.size_hint = (None, 1)
        self.playPauseButton.width = 100

        self.resetButton = Button(text = 'Reiniciar')
        self.resetButton.size_hint = (None, 1)
        self.resetButton.width = 100

        self.recordButton = Button(text = 'Grabar')
        self.recordButton.size_hint = (None, 1)
        self.recordButton.width = 100

        self.connectionBox = ConnectionBox()

        self.add_widget(self.playPauseButton)
        self.add_widget(self.resetButton)
        self.add_widget(self.recordButton)
        self.add_widget(Widget())
        self.add_widget(self.connectionBox)

class LogBox(TextInput):
    def __init__(self):
        super(LogBox, self).__init__()
        self.size_hint = (1, None)
        self.height = 150

class RootWidget(BoxLayout):
    def __init__(self, app):
        super(RootWidget, self).__init__()
        self.app = app

        self.orientation = "vertical"

        self.mainMenu = MainMenu()
        self.logBox = LogBox()
        self.pianoKeyboard = PianoKeyboard()

        self.add_widget(self.mainMenu)
        self.add_widget(self.logBox)
        self.add_widget(self.pianoKeyboard)

class PianoApp(App):
    def __init__(self, *args, **kwargs):
        super(PianoApp, self).__init__(*args, **kwargs)

        self.root = RootWidget(self)

        Clock.schedule_interval(self.arduino_poll, .01)

    def arduino_poll(self, dt):
        data_in = arduino.get()

        if data_in == "CONNECTED":
            self.root.mainMenu.connectionBox.on_connect()
        elif data_in == "DISCONNECTED":
            self.root.mainMenu.connectionBox.on_disconnect()

    def build(self):
        return self.root
