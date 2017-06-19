import os
import pyglet
from pyglet.gl import *
from alarm_manager import AlarmManager
from settings_display import SettingsDisplay
from time_display import TimeDisplay

class WindowManager:
    def __init__(self):
        self.mode = 'clock'
        self._screenOn = True
        self.display = self.timeDisp = TimeDisplay()
        self.alarmSched = AlarmManager(self.alarm)
        self.settingsDisp = SettingsDisplay(self.alarmSched)

    def alarm(self):
        self.screenOn(True)
        self.timeDisp.alarmOn()
        print("CALLED")

    def screenOn(self, b):
        os.system("sudo sh -c 'echo \"{}\" > /sys/class/backlight/soc\:backlight/brightness'".format(1 if b else 0))
        self._screenOn = b

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
        if not self._screenOn:
            self.setMode('clock')
            self.screenOn(True)
        elif event == 'long':
            if self.mode == 'clock' and self.screenOn:
                self.screenOn(False)
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
        if self._screenOn:
            self.display.draw()
        self.alarmSched.run()
