import os
import pyglet
from pyglet.gl import *
from time_display import TimeDisplay
from settings_display import SettingsDisplay

class WindowManager:
    def __init__(self):
        self.mode = 'clock'
        self.settingsDisp = SettingsDisplay()
        self.display = self.timeDisp = TimeDisplay()
        self.screenOn = True

    def setMode(self, m):
        if m == 'settings':
            self.display = self.settingsDisp
        else:
            self.display = self.timeDisp
            if  m == 'bird' and self.mode == 'clock':
                self.display.setBirdMode(True)
            elif  m == 'clock' and self.mode == 'bird':
                self.display.setBirdMode(False)
        self.mode = m

    def registerPress(self, event, x, y):
        if not self.screenOn:
            self.setMode('clock')
            os.system("sudo sh -c 'echo \"1\" > /sys/class/backlight/soc\:backlight/brightness'")
            self.screenOn = True
        elif event == 'long':
            if self.mode == 'clock' and self.screenOn:
                os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc\:backlight/brightness'")
                self.screenOn = False
        elif event == 'drag':
            if self.mode == 'clock':
                self.setMode('bird')
            elif self.mode == 'bird':
                self.setMode('clock')
        elif event == 'short':
            if self.mode != 'settings':
                self.setMode('settings')
                return
        if self.mode == 'settings':
            # return back to clock mode if "done" pressed
            if self.display.press(x, y):
                self.setMode('clock')

    def draw(self):
        self.display.draw()
