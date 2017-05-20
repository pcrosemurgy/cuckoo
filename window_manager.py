import pyglet
from pyglet.gl import *
from time_display import TimeDisplay

# TODO 
# for settings display alpha
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class WindowManager:
    def __init__(self):
        self.mode = 'clock'
        self.display = self.timeDisp = TimeDisplay()
        self.timeDisp.scheduleFuncs()

    def setMode(self, m):
        self.display.unscheduleFuncs()
        if m == 'settings':
            pass
        elif m:
            self.display = self.timeDisp
            if m != self.mode:
                self.timeDisp.birdToggle()
        self.display.scheduleFuncs()
        self.mode = m

    def registerPress(self, event, x, y):
        if event == 'drag':
            if self.mode == 'clock':
                self.setMode('bird')
            elif self.mode == 'bird':
                self.setMode('clock')
        elif event == 'short':
            pass
        elif event == 'long':
            pass

    def draw(self):
        self.display.draw()
