import glob
import pyglet
import datetime
from random import *

class TimeDisplay:
    def __init__(self):
        pyglet.font.add_file('data/cat.ttf')
        catFont = pyglet.font.load('Cat Font')

        self.clouds = CloudBatch()
        self.dateText = None
        self.timeText = None
        self.colon = pyglet.text.Label(':', font_name='Cat Font', font_size=125,
            y=320/2, color=(200, 0, 100, 255),
            anchor_x='center', anchor_y='center')

        self._birdMode = False
        self._showColon = True
        self._bound1 = 0
        self._bound2 = 0
        self.date = ''
        self.hour = ''
        self.minute = ''
        self.s_funcs = {self.update:5, self.colonToggle:0.5, self.clouds.updateSprites:1/60.0}
        self.update()

    def scheduleFuncs(self):
        for f, t in self.s_funcs.iteritems():
            pyglet.clock.schedule_interval(f, t)

    def unscheduleFuncs(self):
        for f in self.s_funcs:
            pyglet.clock.unschedule(f)

    def birdToggle(self):
        self._birdMode = not self._birdMode
        if self._birdMode:
            pyglet.gl.glClearColor(102.0/255, 204.0/255, 1, 1)
        else:
            pyglet.gl.glClearColor(0, 0, 0, 1)

    def colonToggle(self, dt=0):
        self._showColon = not self._showColon

    def update(self, dt=0):
        weekday, month, date, hour, minute = datetime.datetime.now().strftime("%A:%b:%d:%I:%M").split(':')
        hour = str(int(hour))

        if self.date != date: # update date text label
            self.dateText = pyglet.text.Label("{}, {} {}".format(weekday, month, date),
                font_name='Cat Font', font_size=18, x=480/2,
                y=320/2-120, color=(200, 0, 100, 255),
                anchor_x='center', anchor_y='center')
            self.date = date

        if self.hour != hour: # update hour colon bound
            self._bound1 = pyglet.text.Label(hour, font_name='Cat Font', font_size=125).content_width
            self.hour = hour

        if self.minute != minute: # update time text label
            self.timeText = pyglet.text.Label("{} {}".format(hour, minute),
                font_name='Cat Font', font_size=125, x=480/2,
                y=320/2, color=(200, 0, 100, 255),
                anchor_x='center', anchor_y='center')
            self._bound2 = pyglet.text.Label(minute, font_name='Cat Font', font_size=125).content_width
            self.colon.x = 480/2-(self._bound2-self._bound1)/2.0
            self.minute = minute

    def draw(self):
        self.timeText.draw()
        self.dateText.draw()
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

    def updateSprites(self, dt):
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
