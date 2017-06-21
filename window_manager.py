import os
import time
import pigpio
import signal
import subprocess
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
        self.wavProc = None
        # TODO turn off USB
        self.usbOn(False)

    def alarm(self, gpio=None, level=None, tick=None):
        self.screenOn(True)
        self.setMode('alarm')
        # TODO turn on usb
        self.usbOn(True)
        self.wavProc = subprocess.Popen(['while [ 1 ]; do aplay w.wav 2>/dev/null; done;'], stdout=subprocess.PIPE, shell=True)
        self.timeDisp.alarmOn(True)
        pyglet.clock.schedule_once(self.alarmCleanup, 4, False) # TODO make 60 once tested

    def alarmCleanup(self, dt, userInvocation=True):
        if self.mode != 'alarm':
            return
        if userInvocation:
            pyglet.clock.unschedule(self.alarmCleanup)
        else:
            self.screenOn(False)
        os.kill(self.wavProc.pid, signal.SIGKILL)
        # TODO turn off usb
        self.usbOn(False)
        self.pi.write(16, 0)
        self.timeDisp.alarmOn(False)

    def screenOn(self, b):
        os.system("sudo sh -c 'echo \"{}\" > /sys/class/backlight/soc\:backlight/brightness'".format(1 if b else 0))
        self._screenOn = b

    def usbOn(self, b):
        pass

    def setMode(self, m):
        if m == 'settings':
            self.display = self.settingsDisp
        elif m == 'alarm':
            self.display = self.timeDisp
        else:
            self.display = self.timeDisp
            if m == 'bird' and self.mode == 'clock':
                self.display.setBirdMode(True)
            elif  m == 'clock' and self.mode == 'bird':
                self.display.setBirdMode(False)
        self.mode = m

    def registerPress(self, event, x, y):
        if self.mode == 'alarm':
            self.alarmCleanup()
            self.setMode('clock') # TODO setMode to cat gif mode!
        elif not self._screenOn:
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
        else:
            time.sleep(1)
