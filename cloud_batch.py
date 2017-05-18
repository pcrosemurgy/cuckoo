import glob, os
import pyglet
from random import *

# TODO
# add a bunch of funky birds
class CloudBatch(pyglet.graphics.Batch):
    def __init__(self):
        pyglet.graphics.Batch.__init__(self)
        self.sprites = []
        self.birdSprites = []

        for f in glob.glob('data/img/bird*.png'):
            self.birdSprites.append(pyglet.sprite.Sprite(pyglet.image.load(f),
                x=randint(0, 480), y=randint(20, 230)))
        for f in glob.glob('data/img/cloud*.png'):
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load(f),
                x=randint(0, 480), y=randint(20, 300), batch=self))

        s = choice(self.birdSprites)
        s.batch = self
        self.sprites.append(s)

    def updateSprites(self, dt):
        for i, s in enumerate(self.sprites):
            if s.x > 480:
                if i == len(self.sprites)-1:
                    s.batch = None
                    s = self.sprites[-1] = choice(self.birdSprites)
                    s.batch = self
                    s.x = randint(-250, -100)
                    s.y = randint(20, 230)
                else:
                    s.x = randint(-250, -100)
                    s.y = randint(20, 300)
            else:
                vs = 12.0 if i == len(self.sprites)-1 else 22.0
                s.x += vs*dt
