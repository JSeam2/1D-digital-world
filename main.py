# -*- coding: utf-8 -*-#
#-------------------------------------------------------------------------------
# Class: 16F03
# Members: Joshia, Blossom, ShiHui, Angelia, Joshua
#
# Adapted from Licia Leanza androidApp.py
#
#-------------------------------------------------------------------------------
'''
Dictionary for menu items. Right is the name of the panel,
Left is the method to view the panel
'''
SidePanel_AppMenu = {'Temperature':['on_temp',None],
                     'Humidity':['on_hum',None],
                     'Settings':['on_settings',None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1

#################
#     KIVY      #
#################

import kivy
kivy.require('1.8.0')

from kivy.app import App

from kivy.garden.navigationdrawer import NavigationDrawer

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious

from kivy.clock import Clock

# Uncomment/comment for fixed/variable window size
from kivy.config import Config

# Window settings make non-resizable
Config.set('graphics', 'resizable', False)


#################
#     Graph     #
#################
from Graphing import Graphing

'''
Global Values
'''
RootApp = None
url = 'https://my-awesome-project-3e36c.firebaseio.com'
token = 'AxddRZLLd4QR55sNCMXt832N0v759EvheBnWBshR'

'''
Various customized layout widgets corresponding to elements
on heatmapapp.kv
'''

class SidePanel(BoxLayout):
    def __init__(self, **kwargs):
        super(SidePanel, self).__init__(**kwargs)


class MenuItem(Button):
    def __init__(self, **kwargs):
        super(MenuItem, self).__init__( **kwargs)
        self.bind(on_press=self.menuitem_selected)

    def menuitem_selected(self, *args):
        print self.text, SidePanel_AppMenu[self.text], SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        try:
            function_to_call = SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        except:
            print 'Error'
            return
        getattr(RootApp, function_to_call)()


class AppActionBar(ActionBar):
    pass

class ActionMenu(ActionPrevious):
    def menu(self):
        print 'ActionMenu'
        RootApp.toggle_sidepanel()

class ActionQuit(ActionButton):
    def menu(self):
        print 'App quit'
        RootApp.stop()

class MainPanel(BoxLayout):
    pass

class AppArea(FloatLayout):
    pass


'''
Selectable pages and their corresponding methods
'''
class Temperature(FloatLayout):
    '''
    Updates temperature heatmap image when a new image is ready
    '''
    def __init__(self,**kwargs):
        super(Temperature,self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.5)

    def update(self,dt):
        self.ids.tempIMG.reload()


class Humidity(FloatLayout):
    '''
    Updates humidity heatmap image when a new image is ready
    '''
    def __init__(self,**kwargs):
        super(Humidity,self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.5)

    def update(self,dt):
        self.ids.humIMG.reload()

class Settings(FloatLayout):
    '''
    Update global token and url variables and offer the possibility of resetting
    '''
    def update(self):
        '''
        Updates the new url and token
        '''
        global url
        url = self.ids.url.text
        global token
        token = self.ids.token.text

    def default(self):
        '''
        Resets the data incase mistakes are made
        '''
        self.ids.url.text = 'https://my-awesome-project-3e36c.firebaseio.com'
        self.ids.token.text = 'AxddRZLLd4QR55sNCMXt832N0v759EvheBnWBshR'

        global url
        url = 'https://my-awesome-project-3e36c.firebaseio.com'
        global token
        token = 'AxddRZLLd4QR55sNCMXt832N0v759EvheBnWBshR'






class NavDrawer(NavigationDrawer):
    '''
    NavDrawer widget to create the android style menu
    '''
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'




class HeatMapApp(App):

    def build(self):
        global RootApp
        RootApp = self

        # NavigationDrawer
        self.navigationdrawer = NavDrawer()

        # SidePanel
        side_panel = SidePanel()
        self.navigationdrawer.add_widget(side_panel)

        # MainPanel
        self.main_panel = MainPanel()

        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.main_panel)

        # Event manager update every 20 seconds
        print 'configure scheduler'
        self.event = Clock.schedule_interval(self.update, 20)

        return self.navigationdrawer

    def update(self,dt):
        '''
        generates graph. due to outside function call not within clock,
        there may be some delay when updating images
        '''
        try:
            print "------------------"
            print "updating graph..."
            print "------------------"
            global url
            global token
            g = Graphing(url, token)
            print "generate humidity graph..."
            g.gen_hum_graph()
            print 'generate temperature graph...'
            g.gen_temp_graph()
            print "------------------"
            print "update complete..."
            print "------------------"

        except:
            print 'ERRORERRORERRORERRORERRORERRORERROR'
            print ' ...error cannot generate image...'
            print 'ERRORERRORERRORERRORERRORERRORERROR'
            pass

    def toggle_sidepanel(self):
        '''
        self explanatory, toggles the sidepanel
        '''
        self.navigationdrawer.toggle_state()

    def on_temp(self):
        '''
        switches to temperature page
        '''
        print 'VIEW TEMPERATURE DATA...\n'
        self._switch_main_page('Temperature', Temperature)

    def on_hum(self):
        '''
        switches to humidity page
        '''
        print 'VIEW HUMIDITY DATA...\n'
        self._switch_main_page('Humidity', Humidity)
    def on_settings(self):
        '''
        switches to settings page
        '''
        print 'VIEW SETTINGS...\n'
        self._switch_main_page('Settings',  Settings)

    def _switch_main_page(self, key,  panel):
        '''
        Helper function to simplify the creation of page switches
        '''
        self.navigationdrawer.close_sidepanel()
        if not SidePanel_AppMenu[key][id_AppMenu_PANEL]:
            SidePanel_AppMenu[key][id_AppMenu_PANEL] = panel()
        main_panel = SidePanel_AppMenu[key][id_AppMenu_PANEL]
        self.navigationdrawer.remove_widget(self.main_panel)
        self.navigationdrawer.add_widget(main_panel)
        self.main_panel = main_panel



if __name__ == '__main__':
    HeatMapApp().run()

