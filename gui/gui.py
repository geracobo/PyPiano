#!/usr/bin/env python

import kivy
kivy.require('1.7.2')

from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.uix.filechooser import FileChooserListView

from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle

from arduino import Arduino
arduino = Arduino()

from audio import PianoSounds
keys = PianoSounds()

import xml.etree.ElementTree as ET





class PianoKey(Button):
    def __init__(self, key, root):
        super(PianoKey, self).__init__()
        self.root = root

        self.key = key
        self.text = key
        self.color = [0,0,0,1]
        self.background_normal = "gui/img/key.jpg"
        self.background_down = "gui/img/key_down.jpg"

    def key_processing(self):
        if self.root.app.record_mode:
                self.root.logBox.add(self.key)
                return

        if len(self.root.logBox.stack.children) < 1:
            return

        if self.root.logBox.get_current_entry() == None:
            return

        if self.root.app.playing:
            if self.root.logBox.get_current_entry().contains_note(self.key):
                # Send KEY OFF signal
                arduino.send(str.format('-{0}', self.key))

                # Set note to DONE
                self.root.logBox.get_current_entry().set_note_status(self.key, True)

                if self.root.logBox.get_current_entry().is_done():
                    self.root.logBox.current_selection += 1

    def play(self):
        """
        Gets called by the arduino.
        """
        keys[self.key].play()

        self.background_down = "gui/img/key.jpg"
        self.background_normal = "gui/img/key_down.jpg"

        self.key_processing()
        
        Clock.schedule_once(self.play_finish, .3)

    def play_finish(self, dt):
        self.background_normal = "gui/img/key.jpg"
        self.background_down = "gui/img/key_down.jpg"


    def on_state(self, instance, value):
        if value == 'down':
            keys[self.key].play()

            self.key_processing()



class PianoKeyboard(BoxLayout):
    def __init__(self, root):
        super(PianoKeyboard, self).__init__()
        self.root = root

        self.orientation = 'horizontal'
        self.spacing = 1

        self.C4key = PianoKey('C4', self.root)
        self.D4key = PianoKey('D4', self.root)
        self.E4key = PianoKey('E4', self.root)
        self.F4key = PianoKey('F4', self.root)
        self.G4key = PianoKey('G4', self.root)
        self.A4key = PianoKey('A4', self.root)
        self.B4key = PianoKey('B4', self.root)
        self.C5key = PianoKey('C5', self.root)
        self.D5key = PianoKey('D5', self.root)
        self.E5key = PianoKey('E5', self.root)
        self.F5key = PianoKey('F5', self.root)
        self.G5key = PianoKey('G5', self.root)
        self.A5key = PianoKey('A5', self.root)
        self.B5key = PianoKey('B5', self.root)

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
    def __init__(self, root):
        self.root = root
        super(PlayPauseButton, self).__init__()
        self.text = "Reproducir"

    def on_press(self):
        if self.mode == self.PAUSE_MODE:
            self.mode = self.PLAY_MODE
            self.text = "Pausar"
            self.root.app.playing = True
            pass
        elif self.mode == self.PLAY_MODE:
            self.mode = self.PAUSE_MODE
            self.text = "Reproducir"
            self.root.app.playing = False
            pass

class ConnectionBox(BoxLayout):
    def __init__(self):
        super(ConnectionBox, self).__init__()

        self.size_hint = (None, 1)
        self.width = 300

        self.statusLabel = Label()
        self.statusLabel.text = "Desconectado"
        self.statusLabel.color = [1,0,0,1]
        self.statusLabel.size_hint = (None, 1)
        self.statusLabel.width = 110

        self.statusButton = Button()
        self.statusButton.text = "Conectarse"
        self.statusButton.bind(on_press=self.status_pressed)
        self.statusButton.size_hint = (None, 1)
        self.statusButton.width = 110

        self.add_widget(Label(text='Estatus:', size_hint=(None, 1), width=80))
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
    def __init__(self, root):
        super(MainMenu, self).__init__()
        self.root = root
        self.size_hint = (1, None)
        self.height = 40

        self.spacing = 10
        self.padding = [5, 5, 5, 5]

        self.playPauseButton = PlayPauseButton(self.root)
        self.playPauseButton.size_hint = (None, 1)
        self.playPauseButton.width = 100

        self.resetButton = Button(text = 'Reiniciar')
        self.resetButton.size_hint = (None, 1)
        self.resetButton.width = 100
        self.resetButton.bind(on_press=self.on_reset)

        self.recordButton = ToggleButton(text = 'Grabar')
        self.recordButton.size_hint = (None, 1)
        self.recordButton.width = 100
        self.recordButton.bind(state=self.on_record)


        self.saveButton = Button(text="Guardar")
        self.saveButton.size_hint = (None, 1)
        self.saveButton.width = 80
        self.saveButton.bind(on_press=self.on_save)

        self.loadButton = Button(text="Abrir")
        self.loadButton.size_hint = (None, 1)
        self.loadButton.width = 80
        self.loadButton.bind(on_press=self.on_load)


        self.connectionBox = ConnectionBox()

        self.add_widget(self.playPauseButton)
        self.add_widget(self.resetButton)
        self.add_widget(self.recordButton)

        self.add_widget(Widget(size_hint=(None, 1), width=20))

        #self.add_widget(self.saveButton)
        self.add_widget(self.loadButton)

        self.add_widget(Widget())

        self.add_widget(self.connectionBox)

    def on_record(self, instance, state):
        if state == 'down':
            self.root.app.record_mode = True
        else:
            self.root.app.record_mode = False
    def on_reset(self, instance):
        self.root.logBox.current_selection = 1


    def on_load(self, instance):
        self.root._popup = Popup(title='Abrir Archivo')
        self.root._popup.size_hint = (None, None)
        self.root._popup.width = 700
        self.root._popup.height = 400
        self.root._popup.content = FileChooserListView(path='/home/cobo/Programming/Piano/songs', on_submit=self.load)
        self.root._popup.open()

    def load(self, instance, selection, touch):
        self.root._popup.dismiss()
        sel = str(selection[0])
        
        tree = ET.parse(sel)
        song = tree.getroot()

        self.root.logBox.stack.clear_widgets()

        for entry in song:
            notes = list()
            for note in entry:
                notes.append(note.text)
            self.root.logBox.add('|'.join(notes))



    def on_save(self, instance):
        self.root._popup = Popup(title='Guardar Archivo')
        self.root._popup.size_hint = (None, None)
        self.root._popup.width = 700
        self.root._popup.height = 400
        self.root._popup.content = FileChooserListView(path='/home/cobo/Programming/Piano/songs', on_submit=self.save)
        self.root._popup.open()


class LogEntry(Label):
    __events__ = ('on_double_click',)

    def __init__(self, text):
        super(LogEntry, self).__init__()
        self.size_hint=(None, None)
        self.width=100
        self.height=50
        self.text = text

        self.notes = list()

        notesarr = text.split('|')
        for note in notesarr:
            self.notes.append({'note': note, 'done': False})

    def is_done(self):
        for note in self.notes:
            if note['done'] == False:
                return False
        return True

    def contains_note(self, note):
        for n in self.notes:
            if n['note'] == note:
                return True
        return False

    def set_note_status(self, note, done):
        for n in self.notes:
            if n['note'] == note:
                n['done'] = done

    def on_touch_down(self, touch):
        if super(LogEntry, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        if not touch.is_double_tap:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.dispatch('on_double_click')
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            return True
        if super(LogEntry, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(LogEntry, self).on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        return True

    def on_double_click(self):
        self.parent.remove_widget(self)


class LogBox(ScrollView):
    _current_selection = 0


    def __init__(self, root):
        super(LogBox, self).__init__()
        self.root = root
        self.size_hint = (1, None)
        self.height = 150

        self.stack = StackLayout()
        self.stack.orientation = 'lr-tb'
        self.stack.size_hint = (1, None)
        self.stack.bind(minimum_height=self.stack.setter('height'))

        self.add_widget(self.stack)



    def add(self, note):
        self.stack.add_widget(LogEntry(note))

    def get_entry(self, at):
        if at == 0:
            return None
        if at > len(self.stack.children):
            return None
        return self.stack.children[len(self.stack.children)-at]
    def get_current_entry(self):
        return self.get_entry(self.current_selection)

    @property
    def current_selection(self):
        return self._current_selection
    @current_selection.setter
    def current_selection(self, value):
        for child in self.stack.children:
            child.color = [1,1,1,1]

        if value > len(self.stack.children):
            self._current_selection = 0
            return

        self._current_selection = value
        self.stack.children[len(self.stack.children)-value].color = [1,0,0,1]

        # We send a KEY ON signal for each note
        # only if we are on play mode.
        # Reset done status for each note.
        if self.root.app.playing:
            for note in self.get_current_entry().notes:
                note['done'] = False
                arduino.send(str.format("+{0}", note['note']))





class RootWidget(BoxLayout):
    def __init__(self, app):
        super(RootWidget, self).__init__()
        self.app = app

        self.orientation = "vertical"

        self.mainMenu = MainMenu(self)
        self.logBox = LogBox(self)
        self.pianoKeyboard = PianoKeyboard(self)

        self.add_widget(self.mainMenu)
        self.add_widget(self.logBox)
        self.add_widget(self.pianoKeyboard)


class PianoApp(App):
    record_mode = False
    playing = False
    def __init__(self, *args, **kwargs):
        super(PianoApp, self).__init__(*args, **kwargs)

        self.root = RootWidget(self)

        Clock.schedule_interval(self.arduino_poll, .01)

    def arduino_poll(self, dt):
        data = arduino.get()

        for data_in in data:
            if data_in == "CONNECTED":
                self.root.mainMenu.connectionBox.on_connect()
            elif data_in == "DISCONNECTED":
                self.root.mainMenu.connectionBox.on_disconnect()


            if data_in == "C4": self.root.pianoKeyboard.C4key.play()
            if data_in == "D4": self.root.pianoKeyboard.D4key.play()
            if data_in == "E4": self.root.pianoKeyboard.E4key.play()
            if data_in == "F4": self.root.pianoKeyboard.F4key.play()
            if data_in == "G4": self.root.pianoKeyboard.G4key.play()
            if data_in == "A4": self.root.pianoKeyboard.A4key.play()
            if data_in == "B4": self.root.pianoKeyboard.B4key.play()
            if data_in == "C5": self.root.pianoKeyboard.C5key.play()
            if data_in == "D5": self.root.pianoKeyboard.D5key.play()
            if data_in == "E5": self.root.pianoKeyboard.E5key.play()
            if data_in == "F5": self.root.pianoKeyboard.F5key.play()
            if data_in == "G5": self.root.pianoKeyboard.G5key.play()
            if data_in == "A5": self.root.pianoKeyboard.A5key.play()
            if data_in == "B5": self.root.pianoKeyboard.B5key.play()

            data_in = arduino.get()

    def build(self):
        return self.root
