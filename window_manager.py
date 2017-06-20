import os
import pigpio
import pyglet
from pyglet.gl import *
from settings_display import SettingsDisplay
from time_display import TimeDisplay

class WindowManager:
    def __init__(self):
        self.mode = 'clock'
        self._screenOn = True
        self.display = self.timeDisp = TimeDisplay()
        self.settingsDisp = SettingsDisplay()
        self.pi = pigpio.pi()
        self.pi.write(16, 0)
        self.pi.callback(16, func=self.alarm)

    def alarm(self, gpio=None, level=None, tick=None):
        print("CALLED")
        self.screenOn(True)
        self.setMode('clock')
        os.system("while [ 1 ]; do aplay w.wav; done;")
        self.timeDisp.alarmOn()
        # TODO turn on usb then turn off when done
        # TODO handle alarm cleanup

    def screenOn(self, b):
        os.system("sudo sh -c 'echo \"{}\" > /sys/class/backlight/soc\:backlight/brightness'".format(1 if b else 0))
        self._screenOn = b

    def setMode(self, m):
        if m == 'settings':
            self.display = self.settingsDisp
        else:
            self.display = self.timeDisp
            if m == 'bird' and self.mode == 'clock':
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
            if self.display.press(x, y): # return to clock if "done" pressed
                self.setMode('clock')

    def draw(self):
        if self._screenOn:
            self.display.draw()
