# -*- coding: utf-8 -*-#
from kivy.app import App
from kivy.clock import Clock

#-------------------------------------------------------------------------------
# Name:        androidApp.py
# Purpose:     Simple example of a android application skeleton that manages
#              application menu using ActionBar and SidePanelMenu that slides
#              over the main panel
#
# Author:      Licia Leanza
#
# Created:     13-04-2014
# Copyright:   (c) Licia Leanza: 2014
# Licence:     GPL v2
#-------------------------------------------------------------------------------

__author__ = 'licia'

#--------------------------------------------------------------------------
'''dictionary that contains the correspondance between items descriptions
and methods that actually implement the specific function and panels to be
shown instead of the first main_panel
'''
SidePanel_AppMenu = {'voce uno':['on_uno',None],
                     'voce due':['on_due',None],
                     'voce tre':['on_tre',None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1


#--------------------------------------------------------------------------
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import  ObjectProperty

RootApp = None

class SidePanel(BoxLayout):
    pass

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

#

class AppActionBar(ActionBar):
    pass

class ActionMenu(ActionPrevious):
    def menu(self):
        print 'ActionMenu'
        RootApp.toggle_sidepanel()

class ActionQuit(ActionButton):
    pass
    def menu(self):
        print 'App quit'
        RootApp.stop()


class MainPanel(BoxLayout):
    pass

class AppArea(FloatLayout):
    pass

class Page1(FloatLayout):
    pass

class Page2(FloatLayout):
    pass

class Page3(FloatLayout):
    pass

class AppButton(Button):
    nome_bottone = ObjectProperty(None)
    def app_pushed(self):
        print self.text, 'button', self.nome_bottone.state


class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'


class AndroidApp(App):

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

        return self.navigationdrawer

    def toggle_sidepanel(self):
        self.navigationdrawer.toggle_state()

    def on_uno(self):
        print 'UNO... exec'
        self._switch_main_page('Page 1', Page1)

    def on_due(self):
        print 'DUE... exec'
        self._switch_main_page('Page 2', Page2)
    def on_tre(self):
        print 'TRE... exec'
        self._switch_main_page('Page 3',  Page3)

    def _switch_main_page(self, key,  panel):
        self.navigationdrawer.close_sidepanel()
        if not SidePanel_AppMenu[key][id_AppMenu_PANEL]:
            SidePanel_AppMenu[key][id_AppMenu_PANEL] = panel()
        main_panel = SidePanel_AppMenu[key][id_AppMenu_PANEL]
        self.navigationdrawer.remove_widget(self.main_panel)    # FACCIO REMOVE ED ADD perchè la set_main_panel
        self.navigationdrawer.add_widget(main_panel)            # dà un'eccezione e non ho capito perchè
        self.main_panel = main_panel



if __name__ == '__main__':
    AndroidApp().run()
