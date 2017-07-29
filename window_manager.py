import os
import time
import pigpio
import signal
import datetime
import subprocess
import pyglet
from pyglet.gl import *
from time_display import TimeDisplay
from settings_display import SettingsDisplay
from gif_display import GifDisplay

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

    def alarm(self, gpio=None, level=None, tick=None):
        self.screenOn(True)
        self.setMode('alarm')
        os.system('sudo hub-ctrl -h 0 -P 2 -p 1')
        self.wavProc = subprocess.Popen(['W=$(shuf -n1 -e data/sound/*.wav); while [ 1 ]; do aplay $W 2>/dev/null 1>/dev/null; done;'], stdout=subprocess.PIPE, shell=True)
        self.timeDisp.alarmOn(True)
        pyglet.clock.schedule_once(self.alarmCleanup, 39)

    def alarmCleanup(self, dt=None):
        if self.mode != 'alarm':
            return
        if not dt:
            pyglet.clock.unschedule(self.alarmCleanup)
        os.kill(self.wavProc.pid, signal.SIGKILL)
        os.system('sudo hub-ctrl -h 0 -P 2 -p 0')
        self.pi.write(16, 0)
        self.timeDisp.alarmOn(False)

        def reboot(dt):
            os.system('stop.sh')

        if datetime.datetime.today().weekday() > -1: #4: # Friday afternoon
           pyglet.clock.schedule_once(reboot, 5)#10*60)

        self.setMode('cat')

    def screenOn(self, b):
        os.system("sudo sh -c 'echo \"{}\" > /sys/class/backlight/soc\:backlight/brightness'".format(1 if b else 0))
        self._screenOn = b

    def setMode(self, m):
        if m == 'settings':
            self.display = self.settingsDisp
        elif m == 'alarm':
            if self.mode == 'bird':
                self.display.setBirdMode(False)
            self.display = self.timeDisp
        elif m == 'cat':
            self.display = GifDisplay()
        else:
            self.display = self.timeDisp
            if m == 'bird' and self.mode == 'clock':
                self.display.setBirdMode(True)
            elif  m == 'clock' and self.mode == 'bird':
                self.display.setBirdMode(False)
        self.mode = m

    def registerPress(self, event, x, y):
        if self.mode == 'cat':
            return
        if self.mode == 'alarm':
            self.alarmCleanup()
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
            if self.display.draw():
                self.setMode('clock')
        else:
            time.sleep(1)
