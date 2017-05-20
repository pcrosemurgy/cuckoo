import pyglet
from pyglet.gl import *
from time_display import TimeDisplay

# TODO 
# for settings display alpha
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class WindowManager:
    def __init__(self):
        self.mode = ''
        self.display = None
        self.timeDisp = TimeDisplay()
        self.setMode('clock')

    def setMode(self, m):
        if m == 'settings':
            pass
        else:
            self.display = self.timeDisp
            self.timeDisp.setBirdMode(True) if m == 'bird' else self.timeDisp.setBirdMode(False)
        self.mode = m

    def registerPress(self, event, x, y):
        if event == 'drag': # drag: toggle bird mode
            if self.mode == 'clock':
                self.setMode('bird')
            elif self.mode == 'bird':
                self.setMode('clock')
        elif event == 'short': # short hold: settings
            pass
        elif event == 'long': # long hold: tftoff
            pass

    def draw(self):
        self.display.draw()
