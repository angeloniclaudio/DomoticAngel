'''
Showcase of Kivy Features
=========================


'''
from builtins import super, sorted, len
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

# inizializzazione impostazioni
config = ConfigParser()
config.read('config.ini')

dmzurl = ConfigParser()
dmzurl.read('utility/dmzApiModule/domoticzUrls.ini')


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
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        return screen

    def retrive_lights(self):
        dmzapi.loadLights()

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





    def populate_light_page(self, layout):
        def response(req, results):
            if results['status'] == 'OK':
                for elems in results['result']:
                    #print(elems)
                    add_button(elems['Name'],elems['idx'])

        def add_button(name,idx):

            def callback(idx, instance):
                action = dmzurl.get('LIGHT', 'toggle')
                action = action.replace("$IDX", str(idx))
                print(action)
                req = UrlRequest(
                        config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + action)


            if not layout.get_parent_window():
                return
            btn = Button(text=name)
            btn.bind(on_release=partial(callback, idx))
            layout.add_widget(btn)

        req = UrlRequest(
            config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'lights'),
            response)





    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    DomoticXApp().run()
