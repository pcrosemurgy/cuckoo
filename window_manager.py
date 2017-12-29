import os
import glob
import time
import pigpio
import signal
import datetime
import subprocess
import pyglet
import gif_downloader
from threading import Thread
from pyglet.gl import *
from gif_display import *
from time_display import TimeDisplay
from settings_display import SettingsDisplay

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
        if not glob.glob('data/img/day/*.gif'):
            Thread(target=gif_downloader.download).start()

    def alarm(self, gpio=None, level=None, tick=None):
        self.screenOn(True)
        self.setMode('alarm')
        os.system('sudo hub-ctrl -h 0 -P 2 -p 1')
        self.wavProc = subprocess.Popen(['while [ 1 ]; do aplay data/sound/1.wav 2>/dev/null 1>/dev/null; done;'],
            stdout=subprocess.PIPE,
            shell=True)
        self.timeDisp.alarmOn(True)
        pyglet.clock.schedule_once(self.alarmCleanup, 30)

    def alarmCleanup(self, dt=None):
        if self.mode != 'alarm':
            return
        if not dt:
            pyglet.clock.unschedule(self.alarmCleanup)
        os.kill(self.wavProc.pid, signal.SIGKILL)
        os.system('sudo hub-ctrl -h 0 -P 2 -p 0')
        self.pi.write(16, 0)
        self.timeDisp.alarmOn(False)
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
            if self.mode == 'settings' and self.display.press(x, y): # return to clock if "done" pressed
                os.system('sudo shutdown -h now')
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
        if self.mode == 'settings' and self.display.press(x, y): # return to clock if "done" pressed
            self.setMode('clock')

    def draw(self):
        if self._screenOn:
            if self.display.draw():
                self.setMode('clock')
                Thread(target=gif_downloader.download).start()
        else:
            time.sleep(1)
