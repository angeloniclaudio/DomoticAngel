'''
Showcase of Kivy Features
=========================


'''
from time import time
from kivy.app import App
from os.path import join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, \
    ListProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
import utility.dmzApiModule.domzapi as dmzapi
from kivy.uix.button import Button
from kivy.uix.vkeyboard import VKeyboard
from os.path import dirname
from functools import partial
from kivy.properties import ObjectProperty
import time as clock
from kivy.uix.label import Label
from array import array




class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = clock.asctime()




class ButtonAp(Button):
    label = ObjectProperty()
    icon = ObjectProperty()



class DomoticXScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(DomoticXScreen, self).add_widget(*args)


class DomoticXApp(App):
    index = NumericProperty(-1)
    oldindex = ListProperty([])
    current_title = StringProperty()
    time = NumericProperty(0)
    screen_names = ListProperty([])
    hierarchy = ListProperty([])
    use_kivy_settings = False
    crudeclock = IncrediblyCrudeClock()
    Clock.schedule_interval(crudeclock.update, 1)


    def build(self):
        config = self.config
        config.set('KIVY', 'keyboard_mode', 'dock')
        self.title = 'hello world'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'Dashboard', 'Lights', 'Temperatures', 'Scenarios','Rooms'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
                                       '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_screen(self.screen_names.index('Dashboard'))
        vk = VKeyboard(layout='qwerty')


    def build_config(self, config):
        config.setdefaults('CONNECTION', {
            'url': 'http://',
            'username': 'pi',
            'password': 'root'
        })

    def build_settings(self, settings):
        settings.add_json_panel('DomoticX settings', self.config, 'settings_custom.json')


    def focused(self):
        if self.password.focus == True:
            self.vk.on_key_down(self)
        elif self.username.focus == True:
            self.vk.on_key_down(self)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    #def on_current_title(self, instance, value):
     #   self.root.ids.spnr.text = value

#-------------------------------------------- SCREEN MANAGER -----------------------------------------------------------------

    def go_previous_screen(self):
        sm = self.root.ids.sm
        if self.index!=self.screen_names.index('Dashboard'):
            #print(self.oldindex)
            self.go_screen(self.oldindex.pop(-1))
            self.oldindex.pop(-1)
            #print(self.oldindex)

    def go_screen(self, idx):
        self.oldindex.append(self.index)
        #print(self.oldindex)
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

#-------------------------------------------- DASHBOARD -----------------------------------------------------------------

    def populate_dashboard_page(self, layout):
        screens_dash = ['Rooms', 'Scenarios', 'Temperatures']
        icons_dash = ['light.png', 'scene.png', 'temp.png']

        def callback(istance):
            self.go_screen(self.screen_names.index(istance.label.text))

        def create_btn(texto):
            btn = ButtonAp()
            btn.icon.source='data/icons/iconset/size_512/'+icons_dash[screens_dash.index(texto)]
            btn.label.text=texto
            btn.bind(on_release=callback)
            return btn

        for page in screens_dash:
            layout.add_widget(create_btn(page))


#-------------------------------------------- ROOMS -----------------------------------------------------------------


    def populate_room_page(self, layout):

        def roomRequest():
            def serverRoomCallback(results):
                    layout.clear_widgets()
                    for elems in results:
                        add_room_button(elems)
            req=dmzapi.obtainRooms(serverRoomCallback)


        def add_room_button(room):
            btnRoom = ButtonAp()
            btnRoom.info=room
            btnRoom.icon.source='data/icons/iconset/circle.png'
            btnRoom.label.text=room['Name']
            btnRoom.bind(on_release=partial(callback, room['idx']))
            layout.add_widget(btnRoom)

        def callback(roomidx, istance):
            self.go_screen(self.screen_names.index('Lights'))
            self.populate_light_page(roomidx)


        roomRequest()


#-------------------------------------------- LIGHT -----------------------------------------------------------------


    def populate_light_page(self, roomidx):

        def lightRequest(roomIdx):
            def serverResponseCallback(results):
                    for elems in results:
                        layout.clear_widgets()
                        dmzapi.obtainLightStatus(elems['devidx'], add_light_button)
            req = dmzapi.obtainLightsPerRoom(roomIdx, serverResponseCallback)


        def add_light_button(switch):
            btn = ButtonAp()
            btn.info = switch
            btn.icon.source='data/icons/iconset/size_512/light.png'
            btn.label.text=btn.info['Name']
            if btn.info['Status']=='On':
                btn.background_normal = btn.background_down
            btn.bind(on_release=partial(dmzapi.toggleLight, btn.info['idx']))
            layout.add_widget(btn)
            Clock.schedule_interval(partial(timedCheck,btn), 2)


        def update_status(switch):
            def serverResponseCallback(results):
                switch.info = results
                if switch.info['Status']=='On':
                    switch.background_normal = switch.background_down
                else:
                    switch.background_normal = 'atlas://data/images/defaulttheme/button'
            req = dmzapi.obtainLightStatus(switch.info['idx'], serverResponseCallback)

        def timedCheck(but,*t):
            if (self.current_title == 'Lights'):
                update_status(but)

        layout=self.root.ids.sm.current_screen.layout
        lightRequest(roomidx)


#-------------------------------------------- SCENE -----------------------------------------------------------------

    def populate_scene_page(self, layout, mode):

        def serverRequest():
                req = dmzapi.obtainScenes(serverResponseCallback)
                #print('request sent')

        def serverResponseCallback(results):
                layout.clear_widgets()
                for elems in results:
                    add_button(elems)

        def add_button(scene):
            btn = ButtonAp()
            btn.info = scene
            btn.icon.source='data/icons/iconset/size_512/scene.png'
            btn.label.text=scene['Name']
            if scene['Status']=='On':
                btn.background_normal = btn.background_down
            btn.bind(on_release=partial(dmzapi.activateScene, scene['idx']))
            layout.add_widget(btn)


        def compile():
            layout.clear_widgets()
            serverRequest()
            Clock.schedule_interval(timedCheck,2)

        def timedCheck(*t):
            if (self.current_title == 'Scenes'):
                serverRequest()

        if mode == 'first': compile()

#-------------------------------------------- TEMPS -----------------------------------------------------------------

    def populate_temp_page(self, layout, mode):

        def serverRequest():
                req = dmzapi.obtainTemps(serverResponseCallback)
                #print('request sent')

        def serverResponseCallback(results):
                layout.clear_widgets()
                for elems in results:
                        if elems['Type']=='Temp + Humidity + Baro':
                            add_temp_label(elems)

        def add_temp_label(tempItem):
           # print(tempItem)
            lbl = Label()
            lbl.text=tempItem['HardwareName']+' '+str(tempItem['Temp']) +' °C con index '+str(tempItem['idx'])
            layout.add_widget(lbl)


        def compile():
            layout.clear_widgets()
            serverRequest()
            Clock.schedule_interval(timedCheck,2)

        def timedCheck(*t):
            if (self.current_title == 'Temperatures'):
                serverRequest()

        if mode == 'first': compile()


#-------------------------------------------------------------------------------------------------------------

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    DomoticXApp().run()

