import pyglet
from pyglet.gl import *
from time_display import TimeDisplay
from settings_display import SettingsDisplay

# TODO 
# for settings display alpha
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class WindowManager:
    def __init__(self):
        self.mode = 'clock'
        self.settingsDisp = SettingsDisplay()
        self.display = self.timeDisp = TimeDisplay()
        self.timeDisp.scheduleFuncs()

    def setMode(self, m):
        if m == 'settings':
            self.display = self.settingsDisp
        else:
            self.display.unscheduleFuncs()
            self.display = self.timeDisp
            self.display.scheduleFuncs()
            if m != self.mode:
                self.timeDisp.birdToggle()
        self.mode = m

    def registerPress(self, event, x, y):
        if event == 'drag':
            if self.mode == 'clock':
                self.setMode('bird')
            elif self.mode == 'bird':
                self.setMode('clock')
        elif event == 'short':
            if self.mode != 'settings':
                self.setMode('settings')
        elif event == 'long':
            pass
        if self.mode == 'settings':
            self.display.press(x, y)


    def draw(self):
        self.display.draw()
