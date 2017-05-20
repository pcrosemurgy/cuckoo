import pyglet
from pyglet.gl import *

class Icon(pyglet.sprite.Sprite):
    def __init__(self, path, x, y, b=None, visible=True):
        pyglet.sprite.Sprite.__init__(self, pyglet.image.load(path), x, y, batch=b)
        self.visible = visible
        self.waiting = False # avoid double click abuse

    def act(self):
        if self.waiting:
            return
        self.waiting = True
        self.x -= self.width/6
        self.y -= self.height/6
        self.scale = 1.25
        pyglet.clock.schedule_once(self.restoreScale, 0.2)

    def restoreScale(self, dt=0):
        self.waiting = False
        self.scale = 1.0
        self.x += self.width/6
        self.y += self.height/6


class SettingsDisplay:
    def __init__(self):
        self.batchUI = pyglet.graphics.Batch()
        self.bgOff = pyglet.image.load('data/img/bgoff.png')
        self.bgOn = pyglet.image.load('data/img/bgon.png')
        self.bg = self.bgOff
        self.inc = Icon('data/img/inc.png', x=394, y=145, b=self.batchUI)
        self.dec = Icon('data/img/dec.png', x=394, y=70, b=self.batchUI)
        self.done = Icon('data/img/done.png', x=402, y=15, b=self.batchUI)
        self.off = Icon('data/img/off.png', x=405, y=240, b=self.batchUI)
        self.on = Icon('data/img/on.png', x=405, y=240, b=self.batchUI, visible=False)

        def off_func():
            self.bg = self.bgOn
            def f(dt):
                self.off.visible = False
                self.on.visible = True
            pyglet.clock.schedule_once(f, 0.21)

        def on_func():
            self.bg = self.bgOff
            def f(dt):
                self.off.visible = True
                self.on.visible = False
            pyglet.clock.schedule_once(f, 0.21)

        def inc_func():
            pass

        def dec_func():
            pass

        def done_func():
            return True

        self.icons = {self.off:off_func, self.on:on_func, self.inc:inc_func, self.dec:dec_func, self.done:done_func} # only include visible icons

    def unscheduleFuncs(dt):
        pass
    def scheduleFuncs(dt):
        pass

    def isPressed(self, icon, x, y):
        x2 = icon.x
        y2 = icon.y
        w = icon.width
        h = icon.height
        if x >= x2 and y >= y2 and x <= x2+w and y <= y2+h:
            return True
        return False

    def press(self, x, y):
        for i in self.icons:
            if i.visible and self.isPressed(i, x, y):
                i.act()
                return self.icons[i]()

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.bg.blit(0, 0)
        self.batchUI.draw()
