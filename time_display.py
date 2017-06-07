import glob
import pyglet
import datetime
from random import *

class TimeDisplay:
    def __init__(self):
        self.clouds = CloudBatch()
        self._birdMode = False
        self._showColon = True
        self._bound1 = 0
        self._bound2 = 0
        self.date = ''
        self.hour = ''
        self.minute = ''
        self.s_funcs = {self.update:1, self.colonToggle:0.5}

        self.batchLabels = pyglet.graphics.Batch()
        self.dateLabel = pyglet.text.Label('', font_name='Cat Font', font_size=18, x=480/2,
            y=320/2-120, color=(200, 0, 100, 255), anchor_x='center', anchor_y='center',
            batch=self.batchLabels)
        self.timeLabel = pyglet.text.Label('', font_name='Cat Font', font_size=125, x=480/2,
            y=320/2, color=(200, 0, 100, 255), anchor_x='center', anchor_y='center',
            batch=self.batchLabels)
        self.colon = pyglet.text.Label(':', font_name='Cat Font', font_size=125, y=320/2,
            color=(200, 0, 100, 255), anchor_x='center', anchor_y='center')
        self.update()

    def scheduleFuncs(self):
        pyglet.clock.schedule_interval(self.clouds.updateSprites, 1/60.0)
        for f, t in self.s_funcs.iteritems():
            pyglet.clock.schedule_interval(f, t)

    def unscheduleFuncs(self):
        pyglet.clock.unschedule(self.clouds.updateSprites)
        for f in self.s_funcs:
            pyglet.clock.unschedule(f)

    def setBirdMode(self, b):
        if b:
            c = (102.0/255, 204.0/255, 1, 1)
        else:
            c = (0, 0, 0, 1)
        pyglet.gl.glClearColor(*c)
        self.clouds.hide = not b
        self._birdMode = b

    def colonToggle(self, dt=0):
        self._showColon = not self._showColon

    def update(self, dt=0):
        weekday, month, date, hour, minute = datetime.datetime.now().strftime("%A:%b:%d:%I:%M").split(':')
        hour = str(int(hour))
        if self.date != date: # update date text label
            self.dateLabel.text = "%s, %s %s" % (weekday, month, date)
            self.date = date
        if self.hour != hour: # update hour colon bound
            self._bound1 = pyglet.text.Label(hour, font_name='Cat Font', font_size=125).content_width
            self.hour = hour
        if self.minute != minute: # update time text label
            self.timeLabel.text = "%s %02s" % (hour, minute)
            self._bound2 = pyglet.text.Label(minute, font_name='Cat Font', font_size=125).content_width
            self.colon.x = 480/2-(self._bound2-self._bound1)/2.0
            self.minute = minute

    def draw(self):
        self.batchLabels.draw()
        if self._showColon:
            self.colon.draw()
        if self._birdMode:
            self.clouds.draw() 


class CloudBatch(pyglet.graphics.Batch):
    def __init__(self):
        pyglet.graphics.Batch.__init__(self)
        bg, fg = pyglet.graphics.OrderedGroup(0), pyglet.graphics.OrderedGroup(1)

        self.birdSprites = []
        for f in glob.glob('data/img/bird*.png'):
            self.birdSprites.append(pyglet.sprite.Sprite(pyglet.image.load(f),
                x=randint(0, 480), y=randint(20, 230), group=fg))

        s = choice(self.birdSprites)
        s.batch = self
        self.sprites = [s]
        for f in glob.glob('data/img/cloud*.png'):
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(f),
                x=randint(0, 480), y=randint(20, 300), batch=self, group=bg))
        self.hide = True

    def updateSprites(self, dt):
        if self.hide:
            return
        for i, s in enumerate(self.sprites):
            if s.x > 480:
                if i == 0:
                    s.batch = None
                    s = self.sprites[0] = choice(self.birdSprites)
                    s.batch = self
                    s.x = randint(-250, -100)
                    s.y = randint(20, 230)
                else:
                    s.x = randint(-250, -100)
                    s.y = randint(20, 300)
            else:
                vs = 12.0 if i == 0 else 22.0
                s.x += vs*dt
