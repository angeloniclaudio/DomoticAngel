'''
Showcase of Kivy Features
=========================


'''
#from builtins import super, sorted, len
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, \
    ListProperty, Logger
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
import utility.dmzApiModule.domzapi as dmzapi
from kivy.uix.button import Button

from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from os.path import dirname
from functools import partial



class DomoticXScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(DomoticXScreen, self).add_widget(*args)


class DomoticXApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'hello world'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'Dashboard', 'Lights', 'Temperatures', 'Scenarios'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
                                       '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name

    def go_screen(self, idx):
        self.index = idx
        screen =self.load_screen(idx)
        self.root.ids.sm.switch_to(screen, direction='left')
        self.current_title = screen.name

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        return screen


    def populate_dashboard_page(self, layout):
        screens_dash = ['Lights', 'Scenarios', 'Temperatures','Weather']

        def callback(istance):
            self.go_screen(self.screen_names.index(istance.text))

        def create_btn(texto):
            btn = Button(text=texto)
            btn.bind(on_release=callback)
            return btn

        for page in screens_dash:
            layout.add_widget(create_btn(page))





    def populate_light_page(self, layout, mode):

        def serverRequest():
                req = dmzapi.obtainLights(serverResponse)
                print('request sent')

        def serverResponse(req, results):
            if results['status'] == 'OK':
                layout.clear_widgets()
                for elems in results['result']:
                    add_button(elems)

        def add_button(switch):
            colore=[1,1,1,1]
            if switch['Status']=='On': colore=[0.45,1,1,1]
            btn = Button(text=switch['Name'],background_color=colore)
            btn.bind(on_release=partial(dmzapi.toggleLight, switch['idx']))
            layout.add_widget(btn)

        def compile():
            layout.clear_widgets()
            serverRequest()
            Clock.schedule_interval(timedCheck,2)

        def timedCheck(*t):
            if (self.current_title == 'Lights'):
                print(self.current_title )
                serverRequest()

        if mode == 'first': compile()






    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    DomoticXApp().run()
