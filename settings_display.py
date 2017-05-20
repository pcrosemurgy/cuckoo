import pyglet
from pyglet.gl import *

class SettingsDisplay:
    def __init__(self):
        self.batchUI = pyglet.graphics.Batch()
        self.bg = pyglet.image.load('data/img/bg.png')
        x = 400
        y = 315
        self.inc = pyglet.sprite.Sprite(pyglet.image.load('data/img/inc.png'), x=394, y=145, batch=self.batchUI)
        self.dec = pyglet.sprite.Sprite(pyglet.image.load('data/img/dec.png'), x=394, y=70, batch=self.batchUI)
        self.done = pyglet.sprite.Sprite(pyglet.image.load('data/img/done.png'), x=402, y=15, batch=self.batchUI)
        self.off = pyglet.sprite.Sprite(pyglet.image.load('data/img/off.png'), x=405, y=240, batch=self.batchUI)
        self.on = pyglet.sprite.Sprite(pyglet.image.load('data/img/on.png'), x=405, y=240, batch=self.batchUI)
        self.on.visible = False
        self.icons = [self.off, self.inc, self.dec, self.done] # only include visible icons

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
            if self.isPressed(i, x, y):
                i.x -= i.width/6
                i.y -= i.height/6
                i.scale = 1.25
                pyglet.clock.schedule_once(self.restoreScale, 0.2, i)
                break

    def restoreScale(self, dt, icon):
        icon.scale = 1.0
        icon.x += icon.width/6
        icon.y += icon.height/6

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.bg.blit(0, 0)
        self.batchUI.draw()
